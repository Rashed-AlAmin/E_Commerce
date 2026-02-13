from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID


from backend.core.dependencies import get_current_user,get_db

from backend.models.cart import Cart
from backend.models.cart_item import CartItem
from backend.models.product import Product
from backend.models.user import User


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

#add to cart
@router.post("/add/{product_id}")
def add_to_cart(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Check if product already in cart
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=1
        )
        db.add(cart_item)

    db.commit()

    return {"message": "Product added to cart"}

#view cart
@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        return {"items": [], "total": 0}

    items_response = []
    total = 0

    for item in cart.items:
        product = item.product
        subtotal = product.price * item.quantity
        total += subtotal

        items_response.append({
            "product_id": str(product.id),
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "items": items_response,
        "total": total
    }
