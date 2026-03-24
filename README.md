# DataPipeline-Sentinel: Persistent Memory OS for Data Pipelines

![Title](https://raw.githubusercontent.com/aniket-work/DataPipeline-Sentinel/main/images/title-animation.gif)

**DataPipeline-Sentinel** is an experimental open-source PoC demonstrating how to build an "EverMem-style" persistent AI Agent OS. It is specifically designed for Data Engineers to autonomously manage, diagnose, and resolve recurring ETL and data pipeline incidents using Hierarchical Memory.

## The Architecture
The agent uses a 4-tier memory architecture to mimic human reasoning and corporate knowledge retention:

1. **Short-Term Context Buffer (RAM):** Holds immediate workflow variables for active incidents.
2. **Semantic Memory (FAISS):** Stores unstructured past error logs and anomalies as high-dimensional vectors. Allows the agent to instantly retrieve identical or similar historical incidents via cosine similarity.
3. **Episodic Memory (SQLite):** An immutable, chronological audit trail of all agent actions, errors encountered, and ultimate resolutions applied by human engineers.
4. **Declarative Memory (SQLite):** Firm rules, facts, and constraints (e.g., "Always use `infer_schema=True` for MongoDB drift") extracted overnight by a background memory consolidation process.

![Architecture Diagram](https://raw.githubusercontent.com/aniket-work/DataPipeline-Sentinel/main/images/architecture_diagram.png)

## Key Features
- **Automated Memory Consolidation**: A background process that scans recent unstructured episodes (resolutions) and distills them into hard-coded constraints (Declarative logic).
- **Semantic Retrieval**: Uses FAISS indexing to immediately recognize if an obscure pipeline error has been encountered and resolved months prior.
- **Human-in-the-Loop Feedback**: Learns exclusively from what engineers actually do to resolve an incident.

## Project Structure
```text
DataPipeline-Sentinel/
├── main.py              # The simulation lifecycle runner
├── memory_os.py         # FAISS + SQLite Hierarchical Memory implementation
├── sentinel_agent.py    # The Agent logic retrieving and applying memory
├── consolidation.py     # Background distillation job
├── .env                 # API Keys
├── images/              # Generated architecture diagrams and animated GIFs
└── meta_scripts/        # Throwaway scripts used to build assets (Not Pushed)
```

## How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aniket-work/DataPipeline-Sentinel.git
   cd DataPipeline-Sentinel
   ```
2. **Setup virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Run the simulation:**
   ```bash
   python3 main.py
   ```

## Disclaimer
*The views and opinions expressed here are solely my own and do not represent the views, positions, or opinions of my employer or any organization I am affiliated with. The content is based on my personal experience and experimentation and may be incomplete or incorrect. Any errors or misinterpretations are unintentional.*
