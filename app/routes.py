import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.config import UPLOAD_DIR, PRELOADED_DIR, CHROMA_DB_DIR
from app.document_loader import load_single_document, load_documents_from_folder
from app.website_loader import load_website
from app.youtube_loader import load_youtube
from app.rag_engine import RAGEngine


router = APIRouter()
rag_engine = RAGEngine()


class ChatRequest(BaseModel):
    question: str


class WebsiteRequest(BaseModel):
    url: str


class YouTubeRequest(BaseModel):
    url: str


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Multi-Source Intelligent RAG backend is running"
    }


@router.get("/documents")
def list_documents():
    uploaded = [
        file_name
        for file_name in os.listdir(UPLOAD_DIR)
        if os.path.isfile(UPLOAD_DIR / file_name)
    ]

    preloaded = [
        file_name
        for file_name in os.listdir(PRELOADED_DIR)
        if os.path.isfile(PRELOADED_DIR / file_name)
    ]

    return {
        "uploaded_documents": uploaded,
        "preloaded_documents": preloaded,
        "total_documents": len(uploaded) + len(preloaded)
    }


@router.post("/index/preloaded")
def index_preloaded_documents():
    documents = load_documents_from_folder(PRELOADED_DIR)

    if not documents:
        raise HTTPException(
            status_code=404,
            detail="No documents found in preloaded_docs folder"
        )

    result = rag_engine.index_documents(documents)

    return {
        "message": "Preloaded documents indexed successfully",
        **result
    }


@router.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    allowed_extensions = {
        ".pdf",
        ".txt",
        ".docx",
        ".csv"
    }

    all_documents = []
    uploaded_files = []

    for file in files:

        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a supported file."
            )

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        documents = load_single_document(file_path)

        all_documents.extend(documents)
        uploaded_files.append(file.filename)

    result = rag_engine.index_documents(all_documents)

    return {
        "message": "Documents uploaded successfully",
        "files_uploaded": len(uploaded_files),
        "filenames": uploaded_files,
        **result
    }

@router.post("/source/website")
def index_website(request: WebsiteRequest):
    try:
        documents = load_website(request.url)
        result = rag_engine.index_documents(documents)

        return {
            "message": "Website indexed successfully",
            "url": request.url,
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index website: {str(e)}"
        )


@router.post("/source/youtube")
def index_youtube(request: YouTubeRequest):
    try:
        documents = load_youtube(request.url)
        result = rag_engine.index_documents(documents)

        return {
            "message": "YouTube transcript indexed successfully",
            "url": request.url,
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index YouTube video: {str(e)}"
        )


@router.post("/chat")
def chat(request: ChatRequest):
    result = rag_engine.ask(request.question)
    return result


@router.delete("/knowledge-base")
def clear_knowledge_base():
    for file in UPLOAD_DIR.iterdir():
        if file.is_file():
            file.unlink()

    if CHROMA_DB_DIR.exists():
        shutil.rmtree(CHROMA_DB_DIR)

    CHROMA_DB_DIR.mkdir(exist_ok=True)

    return {
        "message": "Knowledge base cleared successfully"
    }