from fastapi import FastAPI
from backend.db.base import Base
from backend.db.session import engine

app = FastAPI(title="Sportswear E-Commerce API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Backend running"}
