# app/schemes/relations_users_roles.py
from pydantic import BaseModel
from typing import Optional, List


# Простые схемы для отношений
class SRoleSimple(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class SUserSimple(BaseModel):
    id: int
    name: str = ""
    email: str


# Основные схемы с отношениями
class SRoleGetWithRels(SRoleSimple):
    users: List[SUserSimple] = []


class SUserGetWithRels(SUserSimple):
    role: Optional[SRoleSimple] = None
    trust_score: float = 5.0