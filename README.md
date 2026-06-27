# 🚀 Multi-Source Intelligent RAG

An enterprise-ready Retrieval-Augmented Generation (RAG) backend built with **FastAPI**, **LangChain**, **ChromaDB**, **Hugging Face Embeddings**, and **Groq LLM**.

This application enables users to build an intelligent knowledge base from multiple sources—including documents, websites, and YouTube videos—and interact with it using natural language queries.

---

# ✨ Features

* 📄 PDF Document Support
* 📝 TXT Document Support
* 📘 DOCX Document Support
* 📊 CSV Document Support
* 🌐 Website Content Indexing
* 🎥 YouTube Transcript Indexing
* 📂 Single & Multiple File Upload
* 📚 Preloaded Knowledge Base
* 🔍 Semantic Search using ChromaDB
* 🤖 AI-Powered Question Answering
* 📑 Source Citation Support
* 🧹 Knowledge Base Reset
* ⚡ RESTful API with FastAPI

---

# 🏗️ System Architecture

```
                Documents
        PDF | TXT | DOCX | CSV
                  │
                  ▼
        Document Loader & Parser
                  │
                  ▼
     Recursive Text Splitter
                  │
                  ▼
 Hugging Face Embedding Model
                  │
                  ▼
             ChromaDB
                  │
                  ▼
        Semantic Retriever
                  │
                  ▼
              Groq LLM
                  │
                  ▼
        AI Generated Response
```

---

# 📂 Supported Knowledge Sources

| Source              | Status |
| ------------------- | ------ |
| PDF                 | ✅      |
| TXT                 | ✅      |
| DOCX                | ✅      |
| CSV                 | ✅      |
| Website             | ✅      |
| YouTube             | ✅      |
| Preloaded Documents | ✅      |

---

# 🛠️ Technology Stack

### Backend

* FastAPI
* Python

### AI & LLM

* LangChain
* Groq
* Hugging Face Embeddings

### Vector Database

* ChromaDB

### Document Processing

* PyPDF
* python-docx
* pandas
* BeautifulSoup4
* youtube-transcript-api

---

# 📡 REST API Endpoints

### Health Check

```
GET /health
```

Returns the server status.

---

### Upload Documents

```
POST /upload
```

Supports:

* PDF
* TXT
* DOCX
* CSV

Supports uploading multiple files in a single request.

---

### Index Website

```
POST /source/website
```

Indexes website content into the knowledge base.

---

### Index YouTube Video

```
POST /source/youtube
```

Extracts and indexes YouTube transcripts.

---

### Index Preloaded Documents

```
POST /index/preloaded
```

Indexes every document inside the `preloaded_docs` folder.

---

### Chat

```
POST /chat
```

Ask questions about indexed knowledge.

Example Request:

```json
{
  "question": "Summarize the uploaded documents."
}
```

---

### List Indexed Documents

```
GET /documents
```

Displays uploaded and preloaded documents.

---

### Clear Knowledge Base

```
DELETE /knowledge-base
```

Removes uploaded documents and clears the vector database.

---

# 📁 Project Structure

```
backend/
│
├── app/
│   ├── config.py
│   ├── document_loader.py
│   ├── rag_engine.py
│   ├── routes.py
│   ├── vector_store.py
│   ├── website_loader.py
│   ├── youtube_loader.py
│   └── main.py
│
├── preloaded_docs/
├── uploads/
├── chroma_db/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

Navigate to the project directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

# 📚 Example Workflow

1. Upload one or more documents.
2. Index websites or YouTube videos.
3. Ask questions using natural language.
4. Receive AI-generated answers with source citations.

---

# 🔮 Future Enhancements

* Modern React frontend
* Streaming AI responses
* Conversation history
* User authentication
* Collection-based knowledge management
* Hybrid Search (BM25 + Vector Search)
* Docker support
* Cloud deployment

---

# 👨‍💻 Author

**Vinay Aluguri**

AI Engineer | Prompt Engineer | LLM Application Developer

---

# 📄 License

This project is licensed under the MIT License.
