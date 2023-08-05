from limsmock.server import app
from limsmock.store import build_db


DB_PATH = "limsmock/demo/test_1"
app.db = build_db(file_path=DB_PATH)
