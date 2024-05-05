from sqlalchemy.orm import Session
from ..db_models.client import Client


def create(
    db_session: Session, email: str, first_name: str, last_name: str
) -> Client:

    client = Client(
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client


def get_client_by_email(db_session: Session, email: str):
    return db_session.query(Client).filter(Client.email == email).first()

