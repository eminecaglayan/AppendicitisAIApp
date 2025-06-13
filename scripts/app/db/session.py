from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Veritabanı motoru oluşturuluyor
engine = create_engine(DATABASE_URL)
# Oturum oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Temel sınıf
Base = declarative_base()


def get_db():
    """Veritabanı oturumu sağlayan bağımlılık"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
