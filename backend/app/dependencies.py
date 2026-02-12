from fastapi import HTTPException, Depends
from .auth import verify_token

def get_current_user(credentials=Depends(verify_token)):
    return credentials

def require_admin(payload=Depends(verify_token)):
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized - Admin only")
    return payload
