from pydantic import BaseModel
from typing import List

class Document(BaseModel):
    id: int
    text: str

class DocumentBatch(BaseModel):
    documents: List[Document]
