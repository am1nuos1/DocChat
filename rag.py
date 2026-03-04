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
            ("system", "以我提供的资料为基础，简洁、专业、全面地回答用户的问题，"
            "如果无法从提供的资料中得到答案，请说“根据我掌握的资料无法回答这个问题”。参考材料：{context}"),
            ("system", "并且我提供用户的对话记录如下:"),
            MessagesPlaceholder("history"),
            ("human", "请回答用户提问：{input}")
        ])
        self.chat_model = ChatTongyi(model = config.chat_model)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_documents(documents):
            if not documents:
                return "无相关资料"
            formatted_docs = ""
            for doc in documents:
                formatted_docs += f"资料片段：{doc.page_content}, 原数据：{doc.metadata}\n\n"
            return formatted_docs
        

        def format_for_retriever(value):
            return value["input"]
        
        def format_for_template(value):
            new_value ={}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value


        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever)| retriever | format_documents
            } | RunnableLambda(format_for_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            message_history_cls=get_history,
            input_message_key= "input",
            history_message_key= "history"
        )

        return conversation_chain
    
if __name__ == "__main__":
    session_config = {
        "configurable": {"session_id": "user_001"},
    }
    rag_service = RagService()
    query = "春天适合穿什么？"
    result = rag_service.chain.invoke({"input": query}, config=session_config)
    print(result)