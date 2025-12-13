import os
import glob
from pathlib import Path
import asyncio
from app import process_and_store_document
from dotenv import load_dotenv

load_dotenv()

def read_markdown_files(docs_path: str):
    """Read all markdown files from the docs folder"""
    md_files = glob.glob(os.path.join(docs_path, "**/*.md"), recursive=True)
    documents = []

    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title from the first line if it's a markdown header
            title = ""
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            if not title:
                title = Path(file_path).stem  # Use filename without extension as title

            documents.append({
                'file_path': file_path,
                'content': content,
                'metadata': {
                    'title': title,
                    'source': file_path
                }
            })
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")

    return documents

def ingest_docs_folder(docs_path: str = "../../docs"):
    """Ingest all markdown files from the docs folder"""
    print(f"Reading markdown files from {docs_path}...")
    documents = read_markdown_files(docs_path)

    print(f"Found {len(documents)} markdown files to process")

    for i, doc in enumerate(documents):
        print(f"Processing ({i+1}/{len(documents)}): {doc['file_path']}")
        try:
            # Process and store the document
            process_and_store_document(
                file_path=doc['file_path'],
                content=doc['content'],
                metadata=doc['metadata']
            )
            print(f"  ✓ Successfully processed {doc['file_path']}")
        except Exception as e:
            print(f"  ✗ Error processing {doc['file_path']}: {str(e)}")

    print(f"\nCompleted ingestion of {len(documents)} documents")

if __name__ == "__main__":
    # Make sure to run this from the backend directory
    docs_path = os.path.join(os.path.dirname(__file__), "..", "docs")
    ingest_docs_folder(docs_path)

# import os
# import glob
# from pathlib import Path
# from app import process_and_store_document
# from dotenv import load_dotenv

# load_dotenv()

# def read_markdown_files(docs_path: str):
#     """Read all markdown files from the docs folder"""
#     md_files = glob.glob(os.path.join(docs_path, "**/*.md"), recursive=True)
#     documents = []

#     for file_path in md_files:
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()

#             # Extract title from first # header
#             title = "Untitled"
#             lines = content.split('\n', 10)  # Only first 10 lines
#             for line in lines:
#                 if line.startswith('# '):
#                     title = line[2:].strip()
#                     break
#             if title == "Untitled":
#                 title = Path(file_path).stem.replace("-", " ").title()

#             documents.append({
#                 'file_path': file_path,
#                 'content': content,
#                 'metadata': {
#                     'title': title,
#                     'source': str(Path(file_path).relative_to(docs_path))
#                 }
#             })
#         except Exception as e:
#             print(f"Error reading {file_path}: {e}")

#     return documents

# def ingest_docs_folder(docs_path: str = "../docs"):
#     """Ingest all markdown files — FIXED for Cohere v3"""
#     full_path = os.path.abspath(docs_path)
#     print(f"Searching for .md files in: {full_path}")
    
#     documents = read_markdown_files(full_path)
#     print(f"Found {len(documents)} files. Starting ingestion...")

#     for i, doc in enumerate(documents, 1):
#         print(f"({i}/{len(documents)}) Processing: {doc['metadata']['title']}")
#         try:
#             process_and_store_document(
#                 file_path=doc['file_path'],
#                 content=doc['content'],
#                 metadata=doc['metadata']
#             )
#             print(f"   Successfully ingested!")
#         except Exception as e:
#             print(f"   Failed: {str(e)}")

#     print(f"\nINGESTION COMPLETE! {len(documents)} documents loaded into Qdrant.")

# if __name__ == "__main__":
#     # Run from backend folder
#     current_dir = Path(__file__).parent
#     docs_path = current_dir.parent / "docs"
#     ingest_docs_folder(str(docs_path))