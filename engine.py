import time
from typing import Dict, List, Tuple
from filters import InjectionSentinel, FactCheckFilter, PlagiarismAuditor, EthicsComplianceLayer

class GuardianEngine:
    def __init__(self):
        self.filters = [
            InjectionSentinel(),
            FactCheckFilter(),
            PlagiarismAuditor(),
            EthicsComplianceLayer()
        ]

    def audit_content(self, title: str, content: str) -> Dict:
        print(f"\n[Guardian-AI] Starting multi-layered audit for: {title}")
        print("-" * 60)
        
        results = []
        overall_status = True
        
        for filter_layer in self.filters:
            print(f"[*] Running {filter_layer.name}...")
            success, message, confidence = filter_layer.process(content)
            
            status = "PASS" if success else "FAIL"
            print(f"    - Status: {status}")
            print(f"    - Log: {message}")
            print(f"    - Confidence: {confidence*100:.1f}%")
            
            results.append({
                "layer": filter_layer.name,
                "success": success,
                "message": message,
                "confidence": confidence
            })
            
            if not success:
                overall_status = False
                print(f"[!] Critical failure in {filter_layer.name}. Halting pipeline.")
                break
        
        print("-" * 60)
        final_status = "APPROVED" if overall_status else "REJECTED"
        print(f"[Guardian-AI] Final Decision: {final_status}")
        
        return {
            "title": title,
            "status": final_status,
            "layers": results
        }
