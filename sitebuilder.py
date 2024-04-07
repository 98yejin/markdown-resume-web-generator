import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

from module import summary_under_direcoty

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"

app = Flask(__name__)
app.config.from_object(__name__)
app.config["FREEZER_DESTINATION"] = "docs"
pages = FlatPages(app)
freezer = Freezer(app)


@app.route("/")
def index():
    about = pages.get("about")
    contact = pages.get("contact")
    education = pages.get("education")
    career_files = summary_under_direcoty("pages/career")
    return render_template(
        "index.html",
        pages=pages,
        data={
            "about": about,
            "contact": contact,
            "education": education,
            "career_files": career_files,
        },
    )


@app.route("/tag/<string:tag>/")
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get("tags", [])]
    return render_template("tag.html", pages=tagged, tag=tag)


@app.route("/career/")
def career():
    career_files = summary_under_direcoty("pages/career")
    return render_template(
        "career.html",
        pages=pages,
        data={
            "career_files": career_files,
        },
    )


@app.route("/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    return render_template("page.html", page=page)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)
