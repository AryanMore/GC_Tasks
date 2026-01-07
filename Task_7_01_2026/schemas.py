from pydantic import BaseModel

class Document(BaseModel):
    id: int
    text: str
