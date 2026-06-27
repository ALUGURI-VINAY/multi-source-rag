from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.config import (
    EMBEDDING_MODEL,
    CHROMA_DB_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RETRIEVER_K
)


class VectorStoreManager:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        self.vector_store = None

    def split_documents(self, documents):

        return self.text_splitter.split_documents(documents)

    def create_vector_store(self, chunks):

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=str(CHROMA_DB_DIR)
        )

        return self.vector_store

    def load_vector_store(self):

        self.vector_store = Chroma(
            persist_directory=str(CHROMA_DB_DIR),
            embedding_function=self.embedding_model
        )

        return self.vector_store

    def get_retriever(self):

        return self.vector_store.as_retriever(
            search_kwargs={
                "k": RETRIEVER_K
            }
        )