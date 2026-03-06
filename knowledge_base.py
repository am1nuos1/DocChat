# Knowledge base
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime



def check_md5(md5_str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()
            if line == md5_str:
                return True

def save_md5(md5_str:str):
    "Save md5"
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_string_md5(input_str, encoding="utf-8"):
    str_byte = input_str.encode(encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_byte)
    md5_hex = md5_obj.hexdigest()
    return md5_hex


class KnowledgeBaseSerive(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory = config.persist_directory
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators= config.separators,
            length_function = len
        )


    def upload_by_str(self, data, filename):
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "File already exists; no upload needed"

        if len(data) > config.max_split_length:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        metadata = {
            "filename": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin"
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata] * len(knowledge_chunks),
        )

        save_md5(md5_hex)
        return f"{filename} uploaded successfully"

    def get_knowledge(self, query):
        pass

    def delete_knowledgebase(self):
        self.chroma.reset_collection()
        if os.path.exists(config.md5_path):
            os.remove(config.md5_path)
        open(config.md5_path, "w", encoding="utf-8").close()
        return "Knowledge base has been cleared and reset"





if "__main__" == __name__:
    service = KnowledgeBaseSerive()
    print()