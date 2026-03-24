from memory_os import HierarchicalMemoryOS

class SentinelAgent:
    """
    Autonomous Data Pipeline Sentinel that monitors incidents,
    retrieves context from Memory OS, and suggests fixes.
    """
    def __init__(self, memory_os: HierarchicalMemoryOS):
        self.memory = memory_os

    def handle_incident(self, pipeline_name, error_log):
        """Main flow when a pipeline fails."""
        # 1. Update Short-Term Context
        self.memory.add_short_term({"event": "incident", "pipeline": pipeline_name, "error": error_log})
        
        # 2. Retrieve Semantic Context (Has this happened before?)
        similar_past_errors = self.memory.retrieve_semantic(error_log)
        
        # 3. Retrieve Declarative Rules (Are there firm rules for this?)
        firm_rules = self.memory.get_declarative_rules("pipeline_fix")
        
        # 4. Formulate Diagnosis & Fix (Simulated LLM Call)
        diagnosis = self._analyze_with_llm(error_log, similar_past_errors, firm_rules)
        
        # 5. Store Incident in Episodic Memory
        episodic_id = self.memory.store_episodic(
            event_type="incident",
            content=f"[{pipeline_name}] failed: {error_log}. Diagnosis: {diagnosis}",
            metadata={"pipeline": pipeline_name, "status": "unresolved"}
        )
        
        # For immediate searchability, we add this to FAISS too
        self.memory.embed_and_store_semantic(error_log, episodic_id)
        
        return diagnosis

    def _analyze_with_llm(self, error_log, past_context, rules):
        """Simulate LLM synthesizing a fix from memory."""
        response = f"Analysis of '{error_log}':\n"
        
        if rules:
            response += f"- Applied Rule: {rules[0]}\n"
            
        if past_context:
            response += f"- Based on {len(past_context)} similar past incidents, recommending known workaround.\n"
        else:
            if "Timeout" in error_log:
                response += "- Novel Timeout detected. Suggest increasing threshold by 50%.\n"
            elif "Schema" in error_log:
                response += "- Novel Schema drift detected. Suggest infer_schema=True.\n"
            else:
                response += "- Unknown failure. Manual engineer review required.\n"
                
        return response
        
    def resolve_incident(self, pipeline_name, resolution):
        """When an engineer confirms a fix, we log it."""
        self.memory.store_episodic(
            event_type="resolution",
            content=f"[{pipeline_name}] fix applied: {resolution}",
            metadata={"pipeline": pipeline_name, "status": "resolved"}
        )
