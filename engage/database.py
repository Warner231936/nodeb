"""MongoDB logging utilities."""

from typing import Any, Dict

try:
    from pymongo import MongoClient
except Exception:  # pragma: no cover
    MongoClient = None

class Database:
    def __init__(self, uri: str):
        self.client = None
        self.db = None
        if MongoClient is None:
            print("pymongo not installed; database disabled.")
            return
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            self.db = self.client.get_default_database()
            self.client.admin.command('ping')
            print("Connected to MongoDB.")
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.client = None

    def log(self, record: Dict[str, Any]):
        if not self.client or not self.db:
            return
        try:
            self.db.logs.insert_one(record)
        except Exception as e:
            print(f"Logging failed: {e}")
