from sqlalchemy.orm import Session
from ..db_models.textextraction import TextExtraction


def create(
    db_session: Session, client_id: int, content: str
) -> TextExtraction:

    text_extraction = TextExtraction(
        client_id=client_id,
        content=content
    )
    db_session.add(text_extraction)
    db_session.commit()
    db_session.refresh(text_extraction)
    return text_extraction


def get_text_extractions_by_client_id(db_session: Session, client_id: int):
    return db_session.query(TextExtraction).filter(TextExtraction.client_id == client_id).all()

