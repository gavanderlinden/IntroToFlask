from flask import Blueprint, render_template_string, abort


templates = {
    "index": """
<title>flask intro</title>
<p>flask app using blueprints</p>
<a href="./hello">hello</a>
""",
    "hello": """
<title>hello page</title>
<p>Hello! Welcome to this Flask introduction</p>
<a href="./">return to index</a>
""",
    "anything": "test"
}


def get_index_app():
    app = Blueprint("index_app", __name__)

    @app.route("/", defaults={"page": "index"})
    @app.route("/<page>")
    def show(page):
        template = templates.get(page)
        if template:
            return render_template_string(template)
        else:
            abort(404)

    return app
