from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.pdf_loader import load_pdf
from app.services.chunking import chunk_text
from app.services.vector_store import create_vector_store

router = APIRouter()

VECTOR_DB = None

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global VECTOR_DB

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_pdf(file_path)
    chunks = chunk_text(text)

    VECTOR_DB = create_vector_store(chunks)

    return {"message": "File processed successfully"}
