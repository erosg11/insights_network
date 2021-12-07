from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from entitys.orm.Base import Base
from entitys.orm.Insight_Tag import insight_tag


class InsightORM(Base):
    __tablename__ = 'insight'
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text)
    data_criacao = Column(DateTime)
    data_modificacao = Column(DateTime)
    tags = relationship('TagORM', secondary=insight_tag, back_populates='insights')

    def __str__(self):
        return f'InsightORM(id={self.id}, texto={self.texto!r}, data_criacao={self.data_criacao!r}, data_modificacao=' \
               f'{self.data_modificacao!r}, tags={self.tags!r})'

    def __repr__(self):
        return self.__str__()
