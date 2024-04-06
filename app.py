from flask import Flask, render_template
from module import (
    read_markdown,
    summary_under_direcoty,
)

app = Flask(__name__)


@app.route("/")
def home():
    about = read_markdown("about.md")
    contact = read_markdown("contact.md")
    career_files = summary_under_direcoty(dirpath="content/career")
    education = read_markdown("education.md")
    return render_template(
        "home.html",
        about=about,
        contact=contact,
        career_files=career_files,
        education=education,
    )


@app.route("/career")
def career():
    return render_template(
        "career.html", career_files=summary_under_direcoty("content/career")
    )


@app.route("/career/<title>")
def career_details(title):
    return render_template(
        "career_details.html",
        content=read_markdown(root="content/career", filepath=f"{title}.md"),
    )


@app.route("/education")
def education():
    return render_template("education.html", content=read_markdown("education.md"))


@app.route("/contact")
def contact():
    return render_template("contact.html", content=read_markdown("contact.md"))


if __name__ == "__main__":
    app.run(debug=True)
    app.config["FREEZER_DESTINATION"] = (
        "static/html"  # Output directory for static files
    )
