from pathlib import Path
from flask import Blueprint, render_template, abort, jsonify, request
from database import get_database
from jinja2 import TemplateNotFound


__dir__ = Path("example5/%s" % __name__).resolve().parent

TEMPLATE_FOLDER = __dir__/"templates"
PAGES = {}
for html_file in TEMPLATE_FOLDER.glob("*.html"):

    if html_file.stem == "base":
        continue

    with html_file.open() as f:
        comment_line = f.readline()
    PAGES[html_file.stem] = {
        "description": comment_line,
        "location": str(html_file)
    }


def get_index_app():
    app = Blueprint("pages", __name__, template_folder=str(TEMPLATE_FOLDER))
    db = get_database("sqlite3")

    @app.route("/", defaults={"page": "index"})
    @app.route("/<page>")
    def show(page):
        template_kwargs = {"pages": PAGES}
        if page == "users":
            template_kwargs.update({"users": db.execute("SELECT * FROM users")})
        try:
            return render_template("%s.html" % page, **template_kwargs)
        except TemplateNotFound:
            abort(404)

    return app


def get_user_app():
    app = Blueprint("user_app", __name__, template_folder=str(TEMPLATE_FOLDER))
    db = get_database("sqlite3")

    @app.route("/user", methods=["POST", "GET"])
    def user():

        # handle POST request
        if request.method == "POST":
            user_name = request.args.get("user_name")
            if user_name:
                result = db.execute(
                    "INSERT INTO users(user_name) VALUES (?)", [user_name], commit=True
                )
                return jsonify(result), 200

        # handle GET request
        if request.method == "GET":
            user_id = request.args.get("user_id")
            user_name = request.args.get("user_name")

            if user_id:
                user = db.execute("SELECT * FROM users WHERE user_id = ?", [user_id])
            elif user_name:
                user = db.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
            else:
                return "Specify user id or user name", 400

            if not user:
                return "User not found", 400
            else:
                return jsonify(user), 200

    return app
