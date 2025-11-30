from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
import httpx
import urllib.parse
import json

app = Flask(__name__)
CORS(app)

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
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        # Translate from English to Vietnamese (auto-detect source if not English)
        try:
            result = translator.translate(text, src='en', dest='vi')
            return jsonify({
                'translated': result.text,
                'src': result.src,
                'dest': result.dest
            })
        except Exception as gt_err:
            # googletrans often fails when Google's web token (TKK) changes.
            # Try a sequence of fallbacks (no API keys required):
            # 1) translate.googleapis.com (public endpoint used by some clients)
            # 2) LibreTranslate public instance
            # Provide clearer error messages and handle non-JSON responses.
            # 1) Try translate.googleapis.com
            g_err_msg = None
            try:
                g_url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=' + urllib.parse.quote(text)
                resp = httpx.get(g_url, timeout=8.0)
                if resp.status_code == 200:
                    try:
                        arr = resp.json()
                        translated = ''.join([seg[0] for seg in arr[0] if seg and len(seg) > 0])
                        return jsonify({'translated': translated, 'src': 'en', 'dest': 'vi', 'fallback': 'translate.googleapis.com'})
                    except Exception:
                        text_body = resp.text.strip()
                        if text_body:
                            return jsonify({'translated': text_body, 'src': 'en', 'dest': 'vi', 'fallback': 'translate.googleapis.com_text'})
            except Exception as g_err:
                g_err_msg = str(g_err)

            # 2) Try LibreTranslate public instance
            try:
                lt_url = 'https://libretranslate.de/translate'
                resp = httpx.post(lt_url, json={
                    'q': text,
                    'source': 'en',
                    'target': 'vi',
                    'format': 'text'
                }, timeout=10.0)
                if resp.status_code == 200:
                    try:
                        j = resp.json()
                        translated = j.get('translatedText') or j.get('translation') or j.get('result')
                        if not translated and isinstance(j, dict):
                            translated = next(iter(j.values()), '')
                        return jsonify({'translated': translated, 'src': 'en', 'dest': 'vi', 'fallback': 'libretranslate'})
                    except json.JSONDecodeError:
                        raw = resp.text.strip()
                        if raw:
                            return jsonify({'translated': raw, 'src': 'en', 'dest': 'vi', 'fallback': 'libretranslate_text'})
                        else:
                            return jsonify({'error': 'LibreTranslate returned empty response'}), 502
                else:
                    lib_msg = resp.text[:400]
                    return jsonify({'error': f'LibreTranslate error {resp.status_code}: {lib_msg}'}), 502
            except Exception as fb_err:
                return jsonify({'error': f'googletrans error: {gt_err}; google_public_fallback_error: {g_err_msg if g_err_msg else "n/a"}; libre_fallback_error: {fb_err}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok', 'message': 'Translation backend running'}), 200


if __name__ == '__main__':
    # Use port 5001 to avoid conflicts with other local servers
    app.run(host='0.0.0.0', port=5001, debug=True)
