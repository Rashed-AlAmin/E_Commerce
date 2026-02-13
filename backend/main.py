from fastapi import FastAPI
from backend.db.session import engine
from backend.routes import (
    test,
    auth,
    product,
    cart)
from backend.db.base import Base
from backend.models.user import User

app = FastAPI()

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(test.router)
app.include_router(product.router)
app.include_router(cart.router)