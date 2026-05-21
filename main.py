from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================
# DATABASE SETUP
# =========================

DATABASE_URL = "YOUR_NEON_DATABASE_URL"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =========================
# MODEL
# =========================

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)

# Create table
Base.metadata.create_all(bind=engine)

# =========================
# APP SETUP
# =========================

app = FastAPI()

# =========================
# REQUEST SCHEMA
# =========================

class LeadCreate(BaseModel):
    name: str
    email: str
    message: str

# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return {"message": "Chukspace API is running"}

@app.post("/submit-lead")
def submit_lead(lead: LeadCreate):
    db = SessionLocal()

    new_lead = Lead(
        name=lead.name,
        email=lead.email,
        message=lead.message
    )

    db.add(new_lead)
    db.commit()
    db.close()

    return {"message": "Lead captured successfully"}
