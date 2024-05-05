from sqlalchemy.orm import Session
from fastapi import APIRouter

from ... import crud
from ...db.session import get_db_func

router = APIRouter()


@router.post("/clients")
async def create_client(
    email: str,
    first_name: str,
    last_name: str,
    db: Session = get_db_func
):
    """
    Create a new client.

    Args:
        email (str): The email address of the client.
        first_name (str): The first name of the client.
        last_name (str): The last name of the client.
        db (Session, optional): The database session instance. Defaults to get_db_func.

    Returns:
        dict: If the client already exists, returns a dictionary with a "detail" key containing an error message.
        dict: If the client is created successfully, returns a dictionary with the client's email, first_name, and last_name.
    """
    existing_client = crud.client.get_client_by_email(db, email)
    if existing_client:
        return {"detail": f"Client with this {existing_client.email} email already exists."}

    client = crud.client.create(
        db_session=db,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    return {
        "email": client.email,
        "first_name": client.first_name,
        "last_name": client.last_name
    }