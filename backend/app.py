from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
import httpx
import urllib.parse
import json
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Activity logging middleware
@app.before_request
def log_request():
    request.start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*80}")
    print(f"[{timestamp}] 📥 FLASK REQUEST")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"Client: {request.remote_addr}")
    if request.method == 'POST' and request.is_json:
        data = request.get_json(silent=True)
        if data:
            print(f"Body preview: {str(data)[:100]}")
    print(f"{'='*80}\n")

@app.after_request
def log_response(response):
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        print(f"✅ Flask response: {response.status_code} (Duration: {duration:.3f}s)\n")
    return response

translator = Translator(service_urls=[
    'translate.google.com',
    'translate.google.co.kr',
    'translate.google.co.jp'
])


@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        print(f"🔤 Translation request: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        if not text:
            print("❌ No text provided")
            return jsonify({'error': 'No text provided'}), 400
        
        # Translate from English to Vietnamese (auto-detect source if not English)
        try:
            result = translator.translate(text, src='en', dest='vi')
            print(f"✅ Translation successful via googletrans")
            return jsonify({
                'translated': result.text,
                'src': result.src,
                'dest': result.dest
            })
        except Exception as gt_err:
            print(f"⚠️  googletrans failed: {str(gt_err)[:100]}, trying fallbacks...")
            # googletrans often fails when Google's web token (TKK) changes.
            # Try a sequence of fallbacks (no API keys required):
            # 1) translate.googleapis.com (public endpoint used by some clients)
            # 2) LibreTranslate public instance
            
            # 1) Try translate.googleapis.com
            g_err_msg = ''
            try:
                g_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q={text}"
                print(f"🔄 Trying Google public API...")
                resp = httpx.get(g_url, timeout=8.0)
                if resp.status_code == 200:
                    try:
                        arr = resp.json()
                        translated = ''.join([seg[0] for seg in arr[0] if seg and len(seg) > 0])
                        print(f"✅ Translation successful via Google public API")
                        return jsonify({'translated': translated, 'src': 'en', 'dest': 'vi', 'fallback': 'translate.googleapis.com'})
                    except Exception:
                        text_body = resp.text.strip()
                        if text_body:
                            print(f"✅ Translation successful via Google public API (text response)")
                            return jsonify({'translated': text_body, 'src': 'en', 'dest': 'vi', 'fallback': 'translate.googleapis.com_text'})
            except Exception as g_err:
                g_err_msg = str(g_err)
                print(f"⚠️  Google public API failed: {g_err_msg[:100]}")

            # 2) Try LibreTranslate public instance
            try:
                lib_url = "https://libretranslate.com/translate"
                lib_data = {"q": text, "source": "en", "target": "vi", "format": "text"}
                print(f"🔄 Trying LibreTranslate...")
                resp = httpx.post(lib_url, json=lib_data, timeout=10.0)
                if resp.status_code == 200:
                    try:
                        j = resp.json()
                        translated = j.get('translatedText') or j.get('translation') or j.get('result')
                        if not translated and isinstance(j, dict):
                            translated = next(iter(j.values()), '')
                        if translated:
                            print(f"✅ Translation successful via LibreTranslate")
                            return jsonify({'translated': translated, 'src': 'en', 'dest': 'vi', 'fallback': 'libretranslate'})
                        else:
                            print(f"❌ LibreTranslate returned empty response")
                            return jsonify({'error': 'LibreTranslate returned empty response'}), 502
                    except json.JSONDecodeError:
                        lib_msg = resp.text[:400]
                        print(f"❌ LibreTranslate JSON decode error: {lib_msg}")
                        return jsonify({'error': f'LibreTranslate JSON error: {lib_msg}'}), 502
                else:
                    lib_msg = resp.text[:400]
                    print(f"❌ LibreTranslate error {resp.status_code}: {lib_msg}")
                    return jsonify({'error': f'LibreTranslate error {resp.status_code}: {lib_msg}'}), 502
            except Exception as fb_err:
                print(f"❌ All translation methods failed")
                return jsonify({'error': f'googletrans error: {gt_err}; google_public_fallback_error: {g_err_msg if g_err_msg else "n/a"}; libre_fallback_error: {fb_err}'}), 500
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok', 'message': 'Translation backend running'}), 200


if __name__ == '__main__':
    # Use port 5001 to avoid conflicts with other local servers
    app.run(host='0.0.0.0', port=5001, debug=True)
