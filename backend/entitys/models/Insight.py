from typing import List
from datetime import datetime

from pydantic import BaseModel

from entitys.models.Tag import Tag


class NewInsight(BaseModel):
    texto: str
    tags: List[str]


class Insight(NewInsight):
    id: int
    data_criacao: datetime
    data_modificacao: datetime
    tags: List[Tag]
