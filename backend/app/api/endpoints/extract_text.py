import os
from typing import Union
from sqlalchemy.orm import Session
from fastapi import File, UploadFile, APIRouter
import docx
import aiohttp
import tempfile
import pdfplumber
from enum import Enum

from ... import crud
from ...db.session import get_db_func
from ...core.email import send_email

router = APIRouter()


class FileType(str, Enum):
    LOCAL = "local"
    REMOTE = "remote"

@router.post(
    "/extract_text",
    summary='Extract Text from doc file.',
)
async def extract_text(
    email: str,
    file_type: FileType,
    file: Union[UploadFile, str] = File(...),
    db: Session = get_db_func
):
    """
    Extract text from a document file (local or remote).

    Args:
        email (str): The email address of the client.
        file_type (FileType): The type of file, either LOCAL or REMOTE.
        file (Union[UploadFile, str]): The file to extract text from. If file_type is LOCAL, this should be an UploadFile instance. If file_type is REMOTE, this should be a URL string.
        db (Session, optional): The database session instance. Defaults to get_db_func.

    Returns:
        dict: If the client is not found, returns a dictionary with a "detail" key containing an error message.
        dict: If the file type is invalid, returns a dictionary with a "detail" key containing an error message.
        dict: If the text extraction is successful, returns a dictionary with the client_id, client_email, and extracted content.

    Raises:
        ValueError: If the file format is unsupported.
    """
    client = crud.client.get_client_by_email(db_session=db, email=email)
    if not client:
        return {"detail": "Client not found"}

    if file_type == FileType.LOCAL:
        # Handle local file upload
        text = await extract_from_file(file)
    elif file_type == FileType.REMOTE:
        # Handle online file URL
        text = await extract_text_from_url(file)
    else:
        return {"detail": "Invalid file type"}

    text_extraction = crud.textextraction.create(
        db_session=db,
        client_id=client.id,
        content=text
    )
    data = {
        'subject': 'Text Extraction Service Update.',
        'body': f"Dear {client.first_name} {client.last_name},<br> \
            Your text extraction task is completed.",
        'to_email': client.email
    }
    send_email(data)

    return {
        'client_id': text_extraction.client_id,
        'client_email': client.email,
        'content': text_extraction.content
    }


async def extract_from_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        text = await extract_from_pdf(file_path)
    elif file_path.endswith((".doc", ".docx")):
        text = await extract_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")
    return text


async def extract_from_pdf(file_path: str) -> str:
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

async def extract_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


async def extract_text_from_url(url: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
        temp_file_path = temp.name
        await download_file(url, temp_file_path)
        text = await extract_from_file(temp_file_path)
        os.unlink(temp_file_path)
        return text


async def download_file(url, dest):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(dest, 'wb') as f:
                    async for data in response.content.iter_chunked(1024):
                        f.write(data)


@router.get(
    "/documents",
    summary="Fetch all documents with extracted content for a user",
)
async def get_documents(email: str, db: Session = get_db_func):
    """
    Fetch all documents with extracted content for a given client.

    Args:
        email (str): The email address of the client.
        db (Session, optional): The database session instance. Defaults to get_db_func.

    Returns:
        dict: If the client is not found, returns a dictionary with a "detail" key containing an error message.
        list: If the client is found, returns a list of documents with extracted content for that client.
    """
    client = crud.client.get_client_by_email(db_session=db, email=email)
    if not client:
        return {"detail": "Client not found"}

    documents = crud.textextraction.get_text_extractions_by_client_id(
        db_session=db,
        client_id=client.id
    )
    return documents

