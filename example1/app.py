from flask import Flask
app = Flask(__name__)


index_template = """
<title>flask intro</title>
<p>single file flask app</p>
<a href="./hello">hello</a>
"""


@app.route("/")
def index():
    return index_template


hello_template = """
<title>hello page</title>
<p>Hello! Welcome to this Flask introduction</p>
<a href="./">return to index</a>
"""


@app.route("/hello")
def hello():
    return hello_template
