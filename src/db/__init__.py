from src.db.mongodb import MongoDBRepository
from src.config import settings

DB_MONGO = MongoDBRepository(settings=settings)
