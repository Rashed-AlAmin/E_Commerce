from fastapi import APIRouter, Depends
from backend.core.dependencies import get_current_user, get_current_admin
from backend.models.user import User

router = APIRouter()

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "is_admin": current_user.is_admin
    }


@router.get("/admin-only")
def admin_route(current_admin: User = Depends(get_current_admin)):
    return {"message": "Welcome admin"}
