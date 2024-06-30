from pydantic import BaseModel

class APIResponse(BaseModel):
    client_ip: str 
    location: str
    greeting: str