# DocChat

DocChat is a lightweight Retrieval-Augmented Generation (RAG) demo built with Streamlit, LangChain, Chroma, and Alibaba DashScope/Tongyi models. It lets you upload text documents into a local knowledge base and then chat with that knowledge base through a conversational question-answering interface.

## What This Project Does

This project is split into two small applications:

- `app_file_uploader.py`: uploads a `.txt` file, splits it into chunks when needed, embeds the text, and stores the vectors in a local Chroma database.
- `app_qa.py`: provides a chat UI that retrieves relevant document chunks from the vector store and sends them, together with chat history, to the LLM for answer generation.

Core capabilities:

- Local knowledge base persistence with Chroma
- Document deduplication with MD5 hashing
- Text chunking for long files
- Retrieval-based Q&A over uploaded content
- Multi-turn chat with file-based conversation history
- Centralized configuration for models, chunking, and retrieval

## Project Structure

```text
DocChat/
├── app_file_uploader.py      # Streamlit app for uploading knowledge files
├── app_qa.py                 # Streamlit app for chat-based document Q&A
├── knowledge_base.py         # Knowledge base ingestion and reset logic
├── rag.py                    # RAG chain composition
├── vector_stores.py          # Chroma retriever wrapper
├── file_history_store.py     # File-backed chat history
├── config_data.py            # Models and runtime configuration
├── data/                     # Chroma database and MD5 tracking
└── chat_history/             # Saved chat sessions
```

## How It Works

1. A user uploads a `.txt` file in the uploader app.
2. The file content is hashed to avoid duplicate ingestion.
3. Long text is split into chunks with `RecursiveCharacterTextSplitter`.
4. Chunks are embedded with DashScope embeddings and stored in a local Chroma collection.
5. In the chat app, the user asks a question.
6. The retriever pulls the most relevant chunks from Chroma.
7. The prompt combines retrieved context, prior chat history, and the current user question.
8. Tongyi generates the final answer.

## Requirements

- Python 3.10+
- A valid `DASHSCOPE_API_KEY`

Python packages used by this project include:

- `streamlit`
- `langchain`
- `langchain-core`
- `langchain-community`
- `langchain-chroma`
- `langchain-text-splitters`
- `chromadb`

You can install them with:

```bash
pip install streamlit langchain langchain-core langchain-community langchain-chroma langchain-text-splitters chromadb
```

## Configuration

Main configuration is defined in `config_data.py`.

Important settings:

- `embedding_model`: embedding model name, currently `text-embedding-v4`
- `chat_model`: chat model name, currently `qwen3-max`
- `collection_name`: Chroma collection name
- `persist_directory`: local vector database directory
- `chunk_size` and `chunk_overlap`: text splitting parameters
- `similarity_top_k`: number of retrieved chunks per query

Before running the project, export your API key:

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

## Usage

### 1. Start the knowledge base uploader

```bash
streamlit run app_file_uploader.py
```

Then:

- Open the Streamlit page in your browser
- Upload a `.txt` file
- Wait for the upload and embedding process to complete

### 2. Start the Q&A app

```bash
streamlit run app_qa.py
```

Then:

- Open the chat page in your browser
- Ask questions related to the uploaded documents
- The app will retrieve relevant snippets and answer using the configured model

## Stored Data

The project stores local runtime data in:

- `data/chroma_db/`: persisted Chroma vector store
- `data/md5.txt`: ingested file hashes for deduplication
- `chat_history/`: serialized chat histories by session ID

## Notes and Limitations

- The uploader currently accepts only `.txt` files.
- There is no dependency lock file in this repository yet.
- The default session ID is fixed as `user_001` unless changed in `config_data.py`.
- `KnowledgeBaseSerive.get_knowledge()` is not implemented.
- The project uses DashScope/Tongyi-specific models, so it is tied to that provider unless refactored.

## Future Improvements

- Add support for PDF, Markdown, and Word documents
- Add a `requirements.txt` or `pyproject.toml`
- Let users manage multiple sessions in the UI
- Add source citation display in answers
- Improve error handling for missing API keys and failed model calls

## License

No license file is included in this repository yet.
