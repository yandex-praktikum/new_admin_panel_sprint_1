import os

dsl = {
        "dbname": "movies_database",
        "user": "app",
        "password": "123qwe",
        "host": "127.0.0.1",
        "port": 5432,
    }

sqlite_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
