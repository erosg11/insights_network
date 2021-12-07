from datetime import datetime
from typing import List

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

    class Config:
        orm_mode = True


class InsightList(BaseModel):
    insights: List[Insight]
