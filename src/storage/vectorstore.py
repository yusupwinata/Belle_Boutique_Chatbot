import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Paths
ABSOLUTE_PATH = Path(__file__).resolve().parent.parent.parent
embeddings_path = os.path.join(ABSOLUTE_PATH, "data", "embeddings")

# API Keys
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "type-your-api-key-here")

class Vectorstore:
    """Save, load, and use the vector store"""
    vectorstore = None

    def __init__(self):
        if not self.vectorstore:
            self.__class__.load_vectorstore()
    
    def check_vectorstore(self) -> None:
        num_docs = self.vectorstore.index.ntotal
        dim = self.vectorstore.index.d
        print(f"Vector store contains {num_docs} documents with {dim} dimensions.\n")

    def similarity_search(self, query: str) -> str:
        result = self.vectorstore.similarity_search(query, k=1)
        return result[0].page_content
    
    def save_vectorstore(self, raw_docs: list) -> None:
        docs = [Document(page_content=text, metadata={"source": f"doc_{i}"}) for i, text in enumerate(raw_docs)]

        new_vectorstore = FAISS.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings()
        )
        new_vectorstore.save_local(embeddings_path)
        self.__class__.load_vectorstore()
        self.check_vectorstore()

    @classmethod
    def load_vectorstore(cls) -> None:
        try:
            cls.vectorstore = FAISS.load_local(
                folder_path=embeddings_path,
                embeddings=OpenAIEmbeddings(),
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            raise Exception(f"Error loading the vector store: {str(e)}")