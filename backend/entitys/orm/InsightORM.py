from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from entitys.orm.Base import Base
from entitys.orm.Insight_Tag import insight_tag


class InsightORM(Base):
    __tablename__ = 'insight'
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text)
    data_criacao = Column(DateTime)
    data_modificao = Column(DateTime)
    tags = relationship('TagORM', secondary=insight_tag, back_populates='insights')
