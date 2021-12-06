from sqlalchemy import Table, Column, ForeignKey

from entitys.orm.Base import Base

insight_tag = Table(
    'insight_tag', Base.metadata,
    Column('insight_id', ForeignKey('insight.id'), primary_key=True),
    Column('tag_id', ForeignKey('tag.id'), primary_key=True)
)
