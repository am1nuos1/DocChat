from langchain_chroma import Chroma
import config_data as config



class VectorStoreService:
    def __init__(self, embedding):
        self.embeddings = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embeddings,
            persist_directory=config.persist_directory

        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_top_k})
    

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model = "text-embedding-v4")
    vector_store_retriever = VectorStoreService(embedding).get_retriever()
    
    res = vector_store_retriever.invoke("What is RAG?")
    print(res)
