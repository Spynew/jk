from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
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
async def register(user: UserRegister):
    print(f"Registration attempt for: {user.email}")
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_pwd = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s, %s)",
            (user.name, user.email, hashed_pwd, datetime.now())
        )
        conn.commit()
        
        return {"message": "Registration successful"}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        print(f"Database error in registration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

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
async def login(user: UserLogin):
    print(f"Login attempt for: {user.email}")
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (user.email,))
        db_user = cursor.fetchone()
        
        if not db_user or not verify_password(user.password, db_user['password']):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_token({"sub": str(db_user['id']), "role": "user"})
        
        return {
            "token": token,
            "user": {
                "id": db_user['id'],
                "name": db_user['name'],
                "email": db_user['email']
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
