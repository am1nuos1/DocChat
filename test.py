from langchain_community.embeddings import DashScopeEmbeddings
import os

print("DASHSCOPE_API_KEY exists:", bool(os.getenv("DASHSCOPE_API_KEY")))

emb = DashScopeEmbeddings(model="text-embedding-v1")
vec = emb.embed_query("Hello")
print(type(vec), len(vec))
print(vec[:5])