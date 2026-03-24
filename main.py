import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from memory_os import HierarchicalMemoryOS
from sentinel_agent import SentinelAgent
from consolidation import MemoryConsolidator

def main():
    console = Console()
    console.print(Panel.fit("[bold cyan]DataPipeline-Sentinel Memory OS Initializing...[/bold cyan]", border_style="cyan"))
    
    # 1. Boot up OS
    mem_os = HierarchicalMemoryOS()
    agent = SentinelAgent(mem_os)
    consolidator = MemoryConsolidator(mem_os)
    
    time.sleep(1)
    
    # 2. Simulate Day 1: Novel Error
    console.print("\n[bold yellow]--- DAY 1: Novel Pipeline Incident ---[/bold yellow]")
    error_log_1 = "MongoDB Extraction Failed: Schema mismatch on 'user_metadata' array."
    console.print(f"[red][Alert][/red] Pipeline 'ETL_User_Sync' failed: {error_log_1}")
    
    time.sleep(1.5)
    console.print("[dim]Agent querying Hierarchical Memory (FAISS + SQLite)...[/dim]")
    diagnosis_1 = agent.handle_incident("ETL_User_Sync", error_log_1)
    console.print(f"[green]Agent Diagnosis:[/green] {diagnosis_1}")
    
    # Engineer applies a fix
    time.sleep(1.5)
    console.print("[bold blue]Engineer Action:[/bold blue] Applied fix -> Updated Spark job with infer_schema=True")
    agent.resolve_incident("ETL_User_Sync", "Updated Spark job with infer_schema=True")
    
    # 3. Simulate Nightly Consolidation Job
    console.print("\n[bold magenta]--- NIGHT 1: Background Memory Consolidation ---[/bold magenta]")
    time.sleep(1.5)
    console.print("[dim]Running batch consolidation over Episodic logs...[/dim]")
    count = consolidator.run_consolidation_cycle()
    console.print(f"[bold magenta]Consolidated {count} episodic events into Declarative Rules.[/bold magenta]")
    
    # 4. Simulate Day 2: Similar Error
    console.print("\n[bold yellow]--- DAY 2: Recurrent Pipeline Incident ---[/bold yellow]")
    error_log_2 = "MongoDB Extraction Failed: Schema mismatch on 'transaction_data' array."
    console.print(f"[red][Alert][/red] Pipeline 'ETL_Tx_Sync' failed: {error_log_2}")
    
    time.sleep(1.5)
    console.print("[dim]Agent querying Hierarchical Memory (FAISS + SQLite)...[/dim]")
    diagnosis_2 = agent.handle_incident("ETL_Tx_Sync", error_log_2)
    console.print(f"[green]Agent Diagnosis:[/green] {diagnosis_2}")
    
    # 5. Output ASCII Table of Memory State
    console.print("\n[bold cyan]--- INTERNAL MEMORY STATE ---[/bold cyan]")
    time.sleep(1)
    
    table = Table(title="Hierarchical Memory OS Snapshot")
    table.add_column("Memory Subsystem", style="cyan", no_wrap=True)
    table.add_column("Entity Count/State", style="magenta")
    table.add_column("Type of Data Supported", style="green")
    
    # Gather stats
    cursor = mem_os.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM episodic_memory")
    episodic_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM declarative_memory")
    declarative_count = cursor.fetchone()[0]
    
    semantic_count = mem_os.index.ntotal
    short_term_count = len(mem_os.short_term_buffer)
    
    table.add_row("Short-term (RAM Buf)", f"{short_term_count} active contexts", "Current active workflow variables")
    table.add_row("Semantic (FAISS)", f"{semantic_count} HNSW Vectors", "Cosine similarity for unstructured logs")
    table.add_row("Episodic (SQLite)", f"{episodic_count} immutable logs", "Chronological audit trail of agent actions")
    table.add_row("Declarative (SQLite)", f"{declarative_count} firm rules", "Hard constraints consolidated from episodes")
    
    console.print(table)
    console.print("\n[bold green]Systems Nominal. Terminating...[/bold green]")
    
if __name__ == "__main__":
    main()
