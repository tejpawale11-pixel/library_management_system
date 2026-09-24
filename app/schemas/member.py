from pydantic import BaseModel

class MemberCreat(BaseModel):  #describes what we expect when creating a member
    name: str
    email: str
    
class MemberResponse(BaseModel):  #describes what our API sends back
    id: int
    name: str
    email: str