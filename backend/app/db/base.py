# Import all the models, so that Base has them before being
# imported by Alembic

from .base_class import Base
from ..db_models.client import Client
from ..db_models.textextraction import TextExtraction