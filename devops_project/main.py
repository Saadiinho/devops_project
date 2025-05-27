from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
import os

# ----------------------
# Configuration DB
# ----------------------

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")  # default to docker-compose service name
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ----------------------
# Modèle SQLAlchemy
# ----------------------


class DomainSkill(Base):
    __tablename__ = "domain_skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


# ----------------------
# Schéma Pydantic
# ----------------------


class DomainSkillSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# ----------------------
# Dépendance DB
# ----------------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------
# FastAPI App
# ----------------------

app = FastAPI()

__version__ = "1.0.0"


@app.get("/healthcheck")
def healthcheck():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return {
            "name": "devops_project API",
            "version": __version__,
            "status": {"application": "running", "database": "connected"},
        }
    except Exception as e:
        return {
            "name": "devops_project API",
            "version": __version__,
            "status": {"application": "running", "database": f"error: {str(e)}"},
        }
    finally:
        db.close()


@app.get("/domain_skills", response_model=List[DomainSkillSchema])
def read_domain_skills(db: Session = Depends(get_db)):
    return db.query(DomainSkill).all()
