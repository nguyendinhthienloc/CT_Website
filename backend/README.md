# Translation backend

This folder contains a minimal Flask backend that provides a translation endpoint using the unofficial `googletrans` library.

Files
- `app.py`: Flask application exposing `POST /translate` expecting JSON `{ "text": "..." }`.
- `requirements.txt`: Python dependencies.

Quick start

1. Create a Python environment (recommended):

   python -m venv .venv
   .venv\Scripts\Activate.ps1   # PowerShell on Windows

2. Install dependencies:

   pip install -r requirements.txt

3. Run the server:

   python app.py

The server listens on port `5000` by default. The frontend can call `http://localhost:5000/translate`.

Notes & alternatives
- `googletrans` is an unofficial wrapper around Google Translate's web API. It usually works for small projects but may be rate-limited or break if Google changes the public endpoints.
- For a production-ready solution, consider using Google Cloud Translate (paid) or another paid translation API. To integrate Google Cloud Translate, you'll need a Google Cloud project, enable the Cloud Translation API, create credentials (API key or service account), and replace the `googletrans` logic with calls to the official client.

Firewall / CORS / Static hosting
- If you serve `index.html` from a static server on a different port (for example `http://localhost:8000`), the included `flask-cors` allows cross-origin requests by default. If you restrict origins on the backend, make sure to whitelist your frontend origin.
