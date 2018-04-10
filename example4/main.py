from flask import Flask, g
from blueprints import get_index_app, get_user_app
from database import add_database, get_database, Sqlite3Database, close_all_databases
from pathlib import Path

__dir__ = Path("example4/%s" % __name__).resolve().parent


app = Flask(__name__)
db = add_database(
    Sqlite3Database, "sqlite3", str(__dir__/"database.db")
)

# add our blueprints
app.register_blueprint(get_index_app(), url_prefix="/pages")
app.register_blueprint(get_user_app(), url_prefix="/users")
