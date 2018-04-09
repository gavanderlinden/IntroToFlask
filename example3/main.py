from flask import Flask
from blueprints import get_index_app

app = Flask(__name__)
app.register_blueprint(get_index_app(), url_prefix="/index_app")
