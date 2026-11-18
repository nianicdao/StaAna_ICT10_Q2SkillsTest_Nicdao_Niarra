"""Non-Metal Element Finder - ICT 10 Q2 Skills Test.

Run:  python app.py   then open http://localhost:8000
Uses only the Python standard library (no installs needed).
"""
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE = Path(__file__).parent

# symbol -> name, atomic number, atomic mass
NON_METALS = {
    "H":  {"name": "Hydrogen",  "number": 1,  "mass": 1.008},
    "He": {"name": "Helium",    "number": 2,  "mass": 4.0026},
    "C":  {"name": "Carbon",    "number": 6,  "mass": 12.011},
    "N":  {"name": "Nitrogen",  "number": 7,  "mass": 14.007},
    "O":  {"name": "Oxygen",    "number": 8,  "mass": 15.999},
    "F":  {"name": "Fluorine",  "number": 9,  "mass": 18.998},
    "Ne": {"name": "Neon",      "number": 10, "mass": 20.180},
    "P":  {"name": "Phosphorus","number": 15, "mass": 30.974},
    "S":  {"name": "Sulfur",    "number": 16, "mass": 32.06},
    "Cl": {"name": "Chlorine",  "number": 17, "mass": 35.45},
    "Ar": {"name": "Argon",     "number": 18, "mass": 39.948},
    "Se": {"name": "Selenium",  "number": 34, "mass": 78.971},
    "Br": {"name": "Bromine",   "number": 35, "mass": 79.904},
    "Kr": {"name": "Krypton",   "number": 36, "mass": 83.798},
    "I":  {"name": "Iodine",    "number": 53, "mass": 126.904},
    "Xe": {"name": "Xenon",     "number": 54, "mass": 131.293},
    "Rn": {"name": "Radon",     "number": 86, "mass": 222},
}


def render_result(symbol):
    """Return the HTML for the result area."""
    if symbol is None:
        return ""
    clean = symbol.strip()
    key = clean.capitalize()
    if not clean:
        return '<div class="note error">Please type a symbol first!</div>'
    info = NON_METALS.get(key)
    if info is None:
        return (f'<div class="note error">&ldquo;{html.escape(clean)}&rdquo; does not '
                'exist in the non-metals list.</div>')
    return f"""
    <div class="result">
      <div class="card c1"><span>Symbol</span><strong>{html.escape(key)}</strong></div>
      <div class="card c2"><span>Element Name</span><strong>{info['name']}</strong></div>
      <div class="card c3"><span>Atomic Number</span><strong>{info['number']}</strong></div>
      <div class="card c4"><span>Atomic Mass</span><strong>{info['mass']}</strong></div>
    </div>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ctype="text/html; charset=utf-8", code=200):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/static/style.css":
            return self._send((BASE / "static" / "style.css").read_text(encoding="utf-8"),
                              "text/css; charset=utf-8")
        if url.path != "/":
            return self._send("Not found", "text/plain", 404)
        symbol = parse_qs(url.query).get("symbol", [None])[0]
        page = (BASE / "index.html").read_text(encoding="utf-8")
        page = page.replace("{{VALUE}}", html.escape(symbol or "", quote=True))
        page = page.replace("{{RESULT}}", render_result(symbol))
        self._send(page)


if __name__ == "__main__":
    print("Open http://localhost:8000")
    HTTPServer(("", 8000), Handler).serve_forever()
