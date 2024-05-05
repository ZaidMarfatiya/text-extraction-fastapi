from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://postgres:root@text-extraction-db-1/text-extraction',
    pool_pre_ping=True,
    pool_size=40,
    pool_recycle=120,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db_func = Depends(get_db)
