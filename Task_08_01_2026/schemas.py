from pydantic import BaseModel
from typing import List


class MarkDownDoc(BaseModel):
    filename: str
    content: str

class MarkDownUpload(BaseModel):
    documents: List[MarkDownDoc]

