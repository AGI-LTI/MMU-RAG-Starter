# RAG Starter Code

This is a minimal implementation of a Retrieval-Augmented Generation (RAG) system that loads documents, creates embeddings, builds a searchable index, retrieves relevant contexts for queries, and generates answers using a language model.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure settings in `config.yaml`
3. Run: `python run_rag.py --query "Your question here"`

## Example Commands

```bash
# Basic usage
python run_rag.py --query "What is machine learning?"

# With custom config
python run_rag.py --query "Explain neural networks" --config custom_config.yaml
```