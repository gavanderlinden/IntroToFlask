from pathlib import Path
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


__dir__ = Path("example3/%s" % __name__).resolve().parent

TEMPLATE_FOLDER = __dir__/"templates"
PAGES = {}
for html_file in TEMPLATE_FOLDER.glob("*.html"):
    with html_file.open() as f:
        comment_line = f.readline()
    PAGES[html_file.stem] = {
        "description": comment_line,
        "location": str(html_file)
    }


def get_index_app():
    app = Blueprint("index_app", __name__, template_folder=str(TEMPLATE_FOLDER))

    @app.route("/", defaults={"page": "index"})
    @app.route("/<page>")
    def show(page):
        try:
            return render_template("%s.html" % page, pages=PAGES)
        except TemplateNotFound:
            abort(404)

    return app
