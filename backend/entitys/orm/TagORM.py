from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from entitys.orm.Base import Base
from entitys.orm.Insight_Tag import insight_tag


class TagORM(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(Text, unique=True)
    insights = relationship('InsightORM', secondary=insight_tag, back_populates='tags')

    def __str__(self):
        return f'TagORM(id={self.id}, nome={self.nome}, insights={self.insights})'
