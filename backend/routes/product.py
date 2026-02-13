from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.product import Product
from backend.schemas.product import ProductCreate, ProductResponse
from backend.core.dependencies import get_db, get_current_admin
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


# Public - anyone can view
@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Product)\
        .filter(Product.is_active == True)\
        .offset(skip)\
        .limit(limit)\
        .all()

# Admin only - create product
@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Admin only - delete product
@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_active = False
    db.commit()
    return {"message": "Product deleted"}

#update product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price

    db.commit()
    db.refresh(product)
    return product

#get producti by id
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
