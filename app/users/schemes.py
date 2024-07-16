from pydantic import BaseModel, EmailStr


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        # orm_model = True
        from_attributes = True
