from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.vector_store import VectorStoreManager


class RAGEngine:
    def __init__(self):
        self.vector_manager = VectorStoreManager()
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL,
            temperature=0.2
        )

        self.prompt = ChatPromptTemplate.from_template(
    """
You are IntelliRAG, an intelligent Multi-Source RAG Assistant.

Use the provided context to answer the question.

Rules:
- Answer using only the context.
- If the context contains related information, use it directly.
- Do not say "not found" if the answer is clearly present in the context.
- Keep the answer short and clear.
- If the answer is truly missing, say:
  "I couldn't find that information in the indexed knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""
)

    def index_documents(self, documents):
        chunks = self.vector_manager.split_documents(documents)
        self.vector_manager.create_vector_store(chunks)

        return {
            "documents_loaded": len(documents),
            "chunks_created": len(chunks)
        }

    def ask(self, question: str):
        self.vector_manager.load_vector_store()

        retriever = self.vector_manager.get_retriever()

        docs = retriever.invoke(question)

        context = "\n\n".join(
            [
                f"Source: {doc.metadata.get('source', 'Unknown')}\n"
                f"Page: {doc.metadata.get('page', 0) + 1}\n"
                f"Content: {doc.page_content}"
                for doc in docs
            ]
        )

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "context": context,
                "question": question
            }
        )

        seen = set()
        sources = []

        for doc in docs:

            source = {
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 0) + 1,
                "file_type": doc.metadata.get("file_type", "Unknown")
            }

            key = (source["source"], source["page"])

            if key not in seen:
                seen.add(key)
                sources.append(source)

        return {
            "answer": response.content,
            "sources": sources
        }