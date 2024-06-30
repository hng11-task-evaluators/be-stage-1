from pydantic import BaseModel, Field
from pydantic.networks import IPv4Address

"""model for this {
    "client_ip": "23.434.34.56",
    "location": "New york",
    "greeting": "No where"
}"""

"""create a score model that will contains points if the json response returned is exactly similar to visitor model

"""
class Visitor(BaseModel):
    client_ip: IPv4Address
    location: str = Field(example="New york", min_length=3, max_length=255)
    greeting: str = Field(example="Hi there", min_length=3, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "client_ip": "23.255.34.56",
                "location": "New york",
                "greeting": "HI there"
            }
        }

class VisitorOut(Visitor):
    visitor_name: str = Field(example="Tom")

class Score(BaseModel):
    visitor_name_score: int = 0
    client_ip_score: int = 0
    location_score: int = 0
    greeting_score: int = 0
    name_in_greeting_score: int = 0
    visitor: VisitorOut