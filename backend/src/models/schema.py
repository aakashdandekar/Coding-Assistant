from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name: str
    mobile: str
    email: EmailStr
    password: str