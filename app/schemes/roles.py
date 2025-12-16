# app/schemes/roles.py
from pydantic import BaseModel
from typing import Optional


class SRoleGet(BaseModel):
    id: int
    name: str


    class Config:
        from_attributes = True


# Для API
class SRoleAdd(BaseModel):
    name: str
