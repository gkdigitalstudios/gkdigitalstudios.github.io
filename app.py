from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os

# Detect "freeze" mode so we can skip non-page routes while building static files
FREEZING = os.getenv("FLASK_FREEZE") == "1"

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY", "replace-this-with-a-strong-secret")

# Use trailing slash style so the freezer writes .../index.html folders
app.url_map.strict_slashes = True


# ---------- Page Routes (freeze-safe) ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/services/")
def services():
    return render_template("services.html")

@app.route("/portfolio/")
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("contact"))

        # Replace with email/DB integration if you deploy a real backend
        print(f"[Contact] {name} <{email}>: {message}")
        flash("Thank you! Your message has been sent.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


# ---------- Non-page utility routes (DISABLED during freezing) ----------
if not FREEZING:
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    @app.route("/robots.txt")
    def robots():
        return send_from_directory(app.static_folder, "robots.txt")

    @app.route("/health")
    def health():
        return {"status": "ok"}


if __name__ == "__main__":
    # Local dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
