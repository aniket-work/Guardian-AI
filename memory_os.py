import sqlite3
import json
import faiss
import numpy as np
from datetime import datetime

class HierarchicalMemoryOS:
    """
    EverMem-Style Persistent Memory OS combining:
    1. Short-term Memory (RAM Buffer)
    2. Episodic Memory (SQLite Event Logs)
    3. Declarative Memory (SQLite Rules & Facts)
    4. Semantic Memory (FAISS Vector Retrieval)
    """
    def __init__(self, db_path="memory_os.db", vector_dim=1536):
        self.db_path = db_path
        self.vector_dim = vector_dim
        self.short_term_buffer = []
        
        # Initialize SQLite (Episodic & Declarative)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
        
        # Initialize FAISS (Semantic)
        self.index = faiss.IndexFlatL2(self.vector_dim)
        # We need a way to map FAISS vector IDs back to SQLite Episodic IDs
        self.id_mapping = {}  # {faiss_id: sqlite_id}
        self.next_faiss_id = 0
        
    def _init_db(self):
        cursor = self.conn.cursor()
        # Episodic Memory: Raw events/logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                event_type TEXT,
                content TEXT,
                metadata TEXT,
                consolidated BOOLEAN DEFAULT 0
            )
        ''')
        # Declarative Memory: Concrete rules/facts derived from episodes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS declarative_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_type TEXT,
                fact_content TEXT,
                confidence REAL
            )
        ''')
        self.conn.commit()

    def add_short_term(self, event):
        """Add to immediate active context."""
        self.short_term_buffer.append(event)
        # Keep buffer manageable
        if len(self.short_term_buffer) > 10:
            self.short_term_buffer.pop(0)

    def store_episodic(self, event_type, content, metadata=None):
        """Permanent append-only ledger of events."""
        metadata_str = json.dumps(metadata) if metadata else "{}"
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO episodic_memory (timestamp, event_type, content, metadata) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), event_type, content, metadata_str)
        )
        self.conn.commit()
        return cursor.lastrowid
        
    def store_declarative(self, fact_type, fact_content, confidence=1.0):
        """Store permanent factual rules."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO declarative_memory (fact_type, fact_content, confidence) VALUES (?, ?, ?)",
            (fact_type, fact_content, confidence)
        )
        self.conn.commit()

    def embed_and_store_semantic(self, text, episodic_id, simulate_embedding=True):
        """Generate vector embedding and store in FAISS."""
        if simulate_embedding:
            # For local simulation, we generate a pseudo-random recognizable vector
            # In production, use OpenAI embedding API
            np.random.seed(hash(text) % (2**32))
            vector = np.random.rand(1, 1536).astype('float32')
        else:
            # Expected API integration here
            vector = np.zeros((1, 1536)).astype('float32') 
            
        faiss.normalize_L2(vector)
        self.index.add(vector)
        self.id_mapping[self.next_faiss_id] = episodic_id
        self.next_faiss_id += 1

    def retrieve_semantic(self, query, top_k=3, simulate_embedding=True):
        """Search FAISS for semantically similar past events."""
        if self.index.ntotal == 0:
            return []
            
        if simulate_embedding:
            # Using the same seed generation to retrieve exact or similar mocks
            np.random.seed(hash(query) % (2**32))
            vector = np.random.rand(1, 1536).astype('float32')
        else:
            vector = np.zeros((1, 1536)).astype('float32')
            
        faiss.normalize_L2(vector)
        distances, indices = self.index.search(vector, top_k)
        
        results = []
        cursor = self.conn.cursor()
        for idx in indices[0]:
            if idx != -1 and idx in self.id_mapping:
                sql_id = self.id_mapping[idx]
                cursor.execute("SELECT content FROM episodic_memory WHERE id = ?", (sql_id,))
                row = cursor.fetchone()
                if row:
                    results.append(row[0])
        return results

    def get_declarative_rules(self, fact_type=None):
        """Retrieve strict rules from SQLite."""
        cursor = self.conn.cursor()
        if fact_type:
            cursor.execute("SELECT fact_content FROM declarative_memory WHERE fact_type = ?", (fact_type,))
        else:
            cursor.execute("SELECT fact_content FROM declarative_memory")
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()
