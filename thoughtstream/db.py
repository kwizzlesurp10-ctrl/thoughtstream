import sqlite3
import ollama
from pathlib import Path
from .config import config
import json
import time

class Database:
    def __init__(self):
        db_path = Path(config.get("database.path", "~/.local/share/thoughtstream/thoughtstream.db")).expanduser()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self.setup()

    def setup(self):
        # Enable VSS if available
        try:
            self.conn.enable_load_extension(True)
            # This assumes sqlite-vss is installed and loadable. 
            # On many systems, this requires specific setup.
            # For now, we'll wrap in try/except to allow basic functionality without VSS
            self.conn.load_extension("vss0") 
        except Exception as e:
            print(f"Warning: Could not load sqlite-vss extension: {e}")

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                source TEXT,
                content TEXT,
                metadata TEXT
            )
        """)
        
        # VSS table would be created here if extension loaded
        # self.conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS vss_entries USING vss0(vector(384))")

    def add_entry(self, source: str, content: str, metadata: dict = None):
        timestamp = time.time()
        meta_json = json.dumps(metadata or {})
        
        cursor = self.conn.execute(
            "INSERT INTO entries (timestamp, source, content, metadata) VALUES (?, ?, ?, ?)",
            (timestamp, source, content, meta_json)
        )
        entry_id = cursor.lastrowid
        
        # Generate embedding and insert into VSS
        self._index_entry(entry_id, content)
        self.conn.commit()

    def _index_entry(self, entry_id: int, content: str):
        try:
            response = ollama.embeddings(model=config.get("llm.embedding_model", "nomic-embed-text"), prompt=content)
            embedding = response["embedding"]
            # Insert into VSS table
            # self.conn.execute("INSERT INTO vss_entries(rowid, vector) VALUES (?, ?)", (entry_id, json.dumps(embedding)))
        except Exception as e:
            # print(f"Error indexing entry: {e}")
            pass

    def search(self, query: str, limit: int = 10):
        # Hybrid search implementation would go here
        # For now, simple text search
        cursor = self.conn.execute(
            "SELECT * FROM entries WHERE content LIKE ? ORDER BY timestamp DESC LIMIT ?",
            (f"%{query}%", limit)
        )
        return cursor.fetchall()

db = Database()

