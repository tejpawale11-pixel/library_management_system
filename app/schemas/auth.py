from pydantic import BaseModel


class RegisterRequest(BaseModel): #information required during registration
    name: str
    email: str
    phone: str
    password: str


class LoginRequest(BaseModel): 
    email: str
    password: str


class UserResponse(BaseModel): #information we are allowed to return to the user
    id: int
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True
        
class TokenResponse(BaseModel): #
    access_token: str
    token_type: str