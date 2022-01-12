from typing import List, Optional

from pydantic import BaseModel


class DocumentBase(BaseModel):
    text: str


class DocumentCreate(DocumentBase):
    pass


class DocumentCreateComplete(DocumentBase):
    """
    This class is needed because the summary is not passed by the user from APIs.
    """
    summary: str


class Document(DocumentCreateComplete):
    id: int

    class Config:
        orm_mode = True
