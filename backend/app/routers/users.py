from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from sqlalchemy import text
from ..database import get_db
from ..models import UserRegister, UserLogin
from ..auth import hash_password, verify_password, create_token, verify_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.options("/register")
async def register_options():
    from starlette.responses import Response
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@router.post("/register")
async def register(user: UserRegister, db=Depends(get_db)):
    print(f"Registration attempt for: {user.email}")
    
    try:
        # Check if user already exists
        result = db.execute(text("SELECT id FROM users WHERE email = :email"), {"email": user.email})
        if result.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_pwd = hash_password(user.password)
        db.execute(
            text("INSERT INTO users (name, email, password, phone, created_at) VALUES (:name, :email, :password, :phone, :created_at)"),
            {
                "name": user.name,
                "email": user.email,
                "password": hashed_pwd,
                "phone": "",  # Default empty phone for now
                "created_at": datetime.now()
            }
        )
        db.commit()
        
        return {"message": "Registration successful"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"Database error in registration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.options("/login")
async def login_options():
    from starlette.responses import Response
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@router.post("/login")
async def login(user: UserLogin, db=Depends(get_db)):
    print(f"Login attempt for: {user.email}")
    
    try:
        result = db.execute(text("SELECT id, name, email, password FROM users WHERE email = :email"), {"email": user.email})
        db_user = result.fetchone()
        
        if not db_user or not verify_password(user.password, db_user[3]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_token({"sub": str(db_user[0]), "role": "user"})
        
        return {
            "token": token,
            "user": {
                "id": db_user[0],
                "name": db_user[1],
                "email": db_user[2]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
