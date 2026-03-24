from memory_os import HierarchicalMemoryOS

class MemoryConsolidator:
    """
    Background job that reviews raw Episodic logs, 
    extracts structural declarative facts, and marks them as consolidated.
    """
    def __init__(self, memory_os: HierarchicalMemoryOS):
        self.memory = memory_os

    def run_consolidation_cycle(self):
        """Scan unconsolidated episodic memory and distill to declarative rules."""
        cursor = self.memory.conn.cursor()
        # Find resolved incidents that haven't been consolidated
        cursor.execute('''
            SELECT id, content FROM episodic_memory 
            WHERE consolidated = 0 AND event_type = 'resolution'
        ''')
        rows = cursor.fetchall()
        
        consolidated_count = 0
        for row in rows:
            record_id, content = row
            
            # Simulated LLM Extraction: Extract a firm rule from the resolution
            if "infer_schema=True" in content:
                rule = "Always use infer_schema=True when dealing with upstream MongoDB drift."
                self.memory.store_declarative("pipeline_fix", rule)
                
            elif "increasing threshold" in content:
                rule = "If API Gateway times out, increase backoff multiplier to 2.0."
                self.memory.store_declarative("pipeline_fix", rule)
                
            # Mark as consolidated
            cursor.execute("UPDATE episodic_memory SET consolidated = 1 WHERE id = ?", (record_id,))
            consolidated_count += 1
            
        self.memory.conn.commit()
        return consolidated_count
