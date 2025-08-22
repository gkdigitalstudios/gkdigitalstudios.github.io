# freeze.py
# Deterministic static export for GitHub Pages (no Frozen-Flask required)
#
# Usage:
#   python freeze.py           -> writes static site to ./build
#   python freeze.py serve     -> quick preview at http://127.0.0.1:8000

import os
import sys
import shutil
from pathlib import Path

# Tell app.py we're "freezing" so it can skip non-page routes.
os.environ["FLASK_FREEZE"] = "1"

from app import app  # noqa: E402

# Which routes to export (must match your page routes in app.py)
ROUTES = [
    "/",            # -> build/index.html
    "/about/",      # -> build/about/index.html
    "/services/",   # -> build/services/index.html
    "/portfolio/",  # -> build/portfolio/index.html
    "/contact/",    # -> build/contact/index.html
]

# Absolute paths to avoid relative path issues
PROJECT_ROOT = Path(__file__).resolve().parent
BUILD_DIR = (PROJECT_ROOT / "build").resolve()
STATIC_SRC = Path(app.static_folder).resolve()        # e.g., PROJECT/static
STATIC_DST = (BUILD_DIR / "static").resolve()


def clean_build():
    if BUILD_DIR.exists():
        print(f"Cleaning existing build folder: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)


def copy_static():
    if STATIC_SRC.exists():
        print("Copying static assets …")
        # Python 3.8+: dirs_exist_ok available; safe since we just cleaned build/
        shutil.copytree(STATIC_SRC, STATIC_DST)
    else:
        print("No /static folder found; skipping static copy.")


def safe_print_written(path: Path):
    """
    Print a human-friendly relative path if possible; otherwise absolute.
    """
    try:
        rel = path.resolve().relative_to(PROJECT_ROOT)
        print(f"Wrote {rel}")
    except Exception:
        print(f"Wrote {path.resolve()}")


def write_html(client, url_path: str):
    """
    Fetch a URL from the Flask app and write it as .../index.html in build/.
    """
    # Normalize URL (leading + trailing slash)
    if not url_path.startswith("/"):
        url_path = "/" + url_path
    if url_path != "/" and not url_path.endswith("/"):
        url_path += "/"

    resp = client.get(url_path)
    if resp.status_code != 200:
        print(f"WARNING: {url_path} -> HTTP {resp.status_code}, skipping")
        return

    # Compute destination dir inside build/
    if url_path == "/":
        dest_dir = BUILD_DIR
    else:
        dest_dir = BUILD_DIR / url_path.strip("/")  # e.g., "about" -> build/about

    dest_dir.mkdir(parents=True, exist_ok=True)
    out_file = dest_dir / "index.html"
    out_file.write_bytes(resp.data)
    safe_print_written(out_file)


def serve_preview():
    # Simple local static server for the ./build folder
    import http.server
    import socketserver

    if not BUILD_DIR.exists():
        print("Build folder not found. Run `python freeze.py` first.")
        sys.exit(1)

    os.chdir(BUILD_DIR)
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving static build at http://127.0.0.1:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "serve":
        serve_preview()
        return

    app.debug = False
    clean_build()
    copy_static()

    print("Freezing site → ./build ...")
    with app.test_client() as client:
        for path in ROUTES:
            write_html(client, path)

    print("Done. Static site is in ./build")


if __name__ == "__main__":
    main()
