from fastapi import FastAPI, HTTPException, Depends, Form
from src.database.db import database
from src.core.auth import get_current_user, hash, check_hash, create_access_token
from src.models.schema import UserSchema

app = FastAPI()

# ===============================================================================
# Authentication & Authorization
# ===============================================================================

@app.post('/auth/register')
async def register(
    data: UserSchema
):
    try:
        collection = database['users']
        exists = await collection.find_one({"email": data.email})

        if exists:
            raise HTTPException(status_code=400, detail=f"User already exists!")
        
        result = await collection.insert_one({
            "name": data.name,
            "mobile": data.mobile,
            "email": data.email,
            "password": hash(data.password)
        })

        token = create_access_token(str(result.inserted_id))
        return {"token": token}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error {e} occurred while registering user.")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post('/auth/login')
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        collection = database['users']
        user = await collection.find_one({
            "email": email
        })

        if not user:
            raise HTTPException(status_code=404, detail="User not Found")
        
        if not check_hash(password, user['password']):
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        
        return {"token": create_access_token(str(user['_id']))}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error {e} occurred while logging in.")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
# ===============================================================================
# Application Program Interface (API)
# ===============================================================================

