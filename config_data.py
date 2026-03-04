md5_path = "C:\\project\\黑马\\黑马rag\\rag project\\data\\md5.txt"




collection_name = "knowledge_base"
persist_directory = "C:\\project\\黑马\\黑马rag\\rag project\\data\\chroma_db"

#spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", "!", "?", ".", ",", ";", ":","！", "？", "。", "，", "；", "："]
max_split_length = 1000


similarity_top_k = 3

embedding_model = "text-embedding-v4"

chat_model = "qwen3-max"