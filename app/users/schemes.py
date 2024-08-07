from pydantic import BaseModel, EmailStr, ConfigDict


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str
    
    # class Config:
    #     # orm_model = True
    #     # from_attributes = True

    model_config = ConfigDict(arbitrary_types_allowed=True)
