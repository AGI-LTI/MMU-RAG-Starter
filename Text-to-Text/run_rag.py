#!/usr/bin/env python3
import argparse
import sys
from src.pipeline import run_rag


def main():
    """
    CLI entrypoint for the RAG system.
    """
    parser = argparse.ArgumentParser(description='Run RAG system with a query')
    parser.add_argument('--query', type=str, required=True, 
                       help='Query to process through the RAG system')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file (default: config.yaml)')
    
    args = parser.parse_args()
    
    try:
        # TODO: Add error handling and logging
        answer = run_rag(args.query, args.config)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()