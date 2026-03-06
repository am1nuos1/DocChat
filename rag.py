from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history



def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt



class RagService:
    def __init__(self):
        self.vector_service = VectorStoreService(embedding = DashScopeEmbeddings(model = config.embedding_model))
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Based on the provided materials, answer the user's question concisely, professionally, and comprehensively. If the answer cannot be found in the materials, reply: 'Based on the available materials, I cannot answer this question.' Reference materials: {context}"),
            ("system", "Additionally, here is the user's conversation history:"),
            MessagesPlaceholder("history"),
            ("human", "Please answer the user's question: {input}")
        ])
        self.chat_model = ChatTongyi(model = config.chat_model)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_documents(documents):
            if not documents:
                return "No relevant materials"
            formatted_docs = ""
            for doc in documents:
                formatted_docs += f"Snippet: {doc.page_content}, Metadata: {doc.metadata}\n\n"
            return formatted_docs
        

        def format_for_retriever(value):
            return value[0].content
        
        def temp1(value):
            print("value in temp1:", value)
            print(type(value))
            return value
        
        def temp2(value):
            print("value in temp2:", value)
            print(type(value))
            return value
        
        def format_for_template(x):
            return {
                "input": x["input"]["input"] if isinstance(x["input"], dict) else x["input"],
                "context": x["context"],
                "history": x["input"].get("history") if isinstance(x["input"], dict) else [],
            }

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | retriever | RunnableLambda(format_documents),
            }
            | RunnableLambda(format_for_template) 
            | self.prompt_template
            | RunnableLambda(print_prompt)
            | self.chat_model
            | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_session_history=get_history,
            input_message_key= "input",
            history_message_key= "history"
        )

        return conversation_chain
    
if __name__ == "__main__":
    session_config = {
        "configurable": {"session_id": "user_001"},
    }
    rag_service = RagService()
    while(input != "exit"):
        query = input("Please enter a question (type 'exit' to quit): ")
        if query == "exit":
            break
        result = rag_service.chain.invoke({"input": query}, config=session_config)
        print(result)