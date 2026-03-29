# Guardian-AI: Multi-Layered Content Integrity Filters for Autonomous Publishing

![Title](https://raw.githubusercontent.com/aniket-work/Guardian-AI/main/images/title_diagram.png)

Guardian-AI is an experimental multi-layered defense system designed to safeguard autonomous publishing pipelines. It utilizes a specialized swarm of integrity agents ("Guardians") to audit AI-generated content for adversarial injections, misinformation, plagiarism, and ethical compliance before publication.

## Core Features

- **Injection Sentinel**: Detects adaptive paraphrased and adversarial prompt injection attacks with pattern-based and heuristic analysis.
- **Fact-Check Filter**: Cross-references claims against trusted knowledge bases and verified sources (simulated using verified sources list).
- **Plagiarism Auditor**: Ensures content originality and originality through similarity indexing.
- **Ethics & Tone Auditor**: Validates content against safety guidelines, toxic language policies, and brand alignment.

## System Architecture

![Architecture](https://raw.githubusercontent.com/aniket-work/Guardian-AI/main/images/architecture_diagram.png)

The Guardian-AI pipeline operates as a sequential filter swarm where each layer must approve the content before it moves to the next. A failure in any layer triggers an immediate halt and rejection report.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/aniket-work/Guardian-AI.git
cd Guardian-AI

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if any)
pip install -r requirements.txt
```

### Running the Audit

```bash
python main.py
```

## Technical Flow

![Sequence](https://raw.githubusercontent.com/aniket-work/Guardian-AI/main/images/sequence_diagram.png)

### The Filtering Process:
1. **The Entry Sentinel**: Scans for "jailbreak" patterns and instruction-bypass attempts.
2. **The Integrity Audit**: Validates factual claims and source attribution.
3. **The Originality Check**: Compares content against a historical database for similarity.
4. **The Behavioral Layer**: Evaluates the tone and safety of the final output.

## Project Structure

```bash
Guardian-AI/
├── main.py          # Entry point and simulation runner
├── engine.py        # Orchestration logic for the filter swarm
├── filters.py       # Implementation of individual integrity layers
├── images/          # Technical diagrams and visual assets
└── README.md        # Professional documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
