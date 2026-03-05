"""
DocChat RAG configuration

Notes:
- Centralizes paths and parameters for knowledge base, text splitting, retrieval, and models.
- Adjusting these values affects persistence locations, chunking strategy, and RAG behavior.
- This file contains only simple constants (no executable logic).
"""

# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
# Embedding model name.
embedding_model = "text-embedding-v4"
# Chat/Completion model name.
chat_model = "qwen3-max"



# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
# Local file path to store processed file MD5 checksums for incremental builds.
# Use workspace-relative paths for portability.
md5_path = "data/md5.txt"

# -----------------------------------------------------------------------------
# Vector Store (Chroma)
# -----------------------------------------------------------------------------
# Collection name used to separate different knowledge domains within one DB.
collection_name = "knowledge_base"
# Directory to persist the Chroma vector database.
persist_directory = "data/chroma_db"

# -----------------------------------------------------------------------------
# Text Splitting (Splitter)
# -----------------------------------------------------------------------------
# Maximum characters per chunk.
chunk_size = 1000
# Overlap characters between adjacent chunks to preserve context.
chunk_overlap = 100
# Preferred separators (high → low priority), covering common English/Chinese punctuation.
separators = [
    "\n\n", "\n", " ", "", "!", "?", ".", ",", ";", ":",
    "！", "？", "。", "，", "；", "：",
]
# Hard cap to avoid extremely long segments.
max_split_length = 1000

# -----------------------------------------------------------------------------
# Retrieval
# -----------------------------------------------------------------------------
# Number of most similar chunks to retrieve (Top-K).
similarity_top_k = 3

# -----------------------------------------------------------------------------
# Session
# -----------------------------------------------------------------------------
# Default session configuration; can be overridden at runtime.
session_config = {
    "configurable": {"session_id": "user_001"},
}