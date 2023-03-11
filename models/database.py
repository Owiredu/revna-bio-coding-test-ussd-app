import sqlite3
from pathlib import Path

# get the sqlite database connection handle
database_path: Path = Path(".") / "db.sqlite"
db_conn_handle: sqlite3.Connection = sqlite3.connect(database=database_path)
