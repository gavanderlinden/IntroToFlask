import sqlite3
from pathlib import Path


__dir__ = Path("example4/%s" % __name__).resolve().parent

DATABASES = {}


def load_queries():
    for query_path in (__dir__/"queries").glob("*.sql"):
        with open(query_path) as query_file:
            query = query_file.read()
        yield query_path.stem, query

QUERIES = {
    query_name: query for query_name, query in load_queries()
}


class Sqlite3Database(object):
    _client = None

    def __init__(self, path):
        self._database_path = path
        for query_name, query in QUERIES.items():
            if query_name.startswith("create"):
                self.execute(query, commit=True)

    @property
    def client(self):
        client = self._client
        if client is None:
            client = self._client = sqlite3.connect(self._database_path)

        return client

    @property
    def cursor(self):
        return self.client.cursor()

    def execute(self, query, args=(), commit=False):
        cur = self.cursor
        cur.execute(query, args)
        result = cur.fetchall()
        cur.close()

        # commit data to file
        if commit:
            self.client.commit()

        return result

    def execute_many(self, query, args=(), commit=False):
        cur = self.cursor
        cur.executemany(query, args)
        result = cur.fetchall()
        cur.close()

        # commit data to file
        if commit:
            self.client.commit()

        return result

    def close(self):
        db = self._client
        if db is not None:
            db.close()


def add_database(database_class, database_name, database_uri):

    DATABASES[database_name] = database = {
        "uri": str(database_uri),
        "client": database_class(str(database_uri))
    }

    return database["client"]


def get_database(database_name):

    if not DATABASES:
        raise BaseException("No databases configured")

    database = DATABASES.get(database_name)
    if database:
        return database["client"]
    else:
        raise BaseException("Database %s does not exist" % database_name)


def close_all_databases():
    for database_name, database in DATABASES.items():
        print("Closing database:", database_name)
        database["client"].close()
