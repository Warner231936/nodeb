"""MongoDB logging utilities."""

from typing import Any, Dict, Optional

try:
    from pymongo import MongoClient
except Exception:  # pragma: no cover
    MongoClient = None

class Database:
    """Simple wrapper around :class:`pymongo.MongoClient`.

    The database name can be provided separately from the URI so that a
    generic connection string like ``mongodb://localhost:27017`` may be
    used.  If ``name`` is omitted the client will attempt to use the
    default database from the URI.
    """

    def __init__(self, uri: str, name: Optional[str] = None, timeout_ms: Optional[int] = None):
        self.client = None
        self.db = None
        if MongoClient is None:
            print("pymongo not installed; database disabled.")
            return
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)
            self.db = self.client[name] if name else self.client.get_default_database()
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
