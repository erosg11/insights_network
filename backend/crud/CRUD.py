from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from entitys import InsightORM, TagORM, NewInsight, Tag


def create_tag(db: Session, name: str) -> TagORM:
    tag = TagORM()
    tag.nome = name
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def _create_tag_in_memory(name: str) -> TagORM:
    tag = TagORM()
    tag.nome = name
    return tag


def create_multiple_tags(db: Session, names: List[str]) -> List[TagORM]:
    tags = [_create_tag_in_memory(name) for name in names]
    db.add_all(tags)
    db.commit()
    tags = [db.refresh(x) for x in tags]
    return tags


def _get_tags_or_insert(db: Session, new_insight_tags: List[str]):
    tags = db.query(TagORM).filter(TagORM.nome.in_(new_insight_tags)).all()  # type: List[TagORM]
    if len(tags) < len(new_insight_tags):
        found_tag_names = {x.nome for x in tags}
        new_tags = set(new_insight_tags)
        tags_to_insert = list(new_tags - found_tag_names)
        tags += create_multiple_tags(db, tags_to_insert)
    return tags


def create_insight(db: Session, new_insight: NewInsight):
    insight = InsightORM()
    insight.texto = new_insight.texto
    insight.data_modificao = insight.data_criacao = datetime.now()
    tags = _get_tags_or_insert(db, new_insight.tags)
    insight.tags = tags
    db.add(insight)
    db.commit()
    db.refresh(insight)
    return insight


def _get_insight_by_id(db: Session, id: int):
    return db.query(InsightORM).filter(InsightORM.id == id)


def get_insight_by_id(db: Session, id: int) -> InsightORM:
    return _get_insight_by_id(db, id).first()


def delete_insight(db: Session, id: int):
    _get_insight_by_id(db, id).delete()
    db.commit()


def update_insight(db: Session, id: int, new_insight: NewInsight) -> InsightORM:
    pointer_insight = _get_insight_by_id(db, id)
    old_insight = pointer_insight.first()  # type: Optional[InsightORM]
    if old_insight is None:
        raise ValueError(f'Insight {id} not found')
    update = {}
    if old_insight.texto != new_insight.texto:
        update['texto'] = new_insight.texto
    old_tags = {x.nome for x in old_insight.tags}
    new_tags = set(new_insight.tags)
    if new_tags != old_tags:
        tags = old_insight.tags
        tags_to_remove = old_tags - new_tags
        if tags_to_remove:
            tags = [x for x in tags if x.nome not in tags_to_remove]
        tags_to_insert = new_tags - old_tags
        if tags_to_insert:
            tags += _get_tags_or_insert(db, list(tags_to_insert))
        update['tags'] = tags
    if not update:
        raise ValueError('No update')
    update['data_modificao'] = datetime.now()
    pointer_insight.update(update)
    db.commit()
    db.refresh(old_insight)
    return old_insight


def list_cards(db: Session, tags, skip=0, limit=10) -> List[InsightORM]:
    return db.query(InsightORM).join(TagORM).filter(TagORM.nome.in_(tags)).skip(skip).limit(limit).all()


def _get_tag_by_id(db, id):
    return db.query(TagORM).filter(TagORM.id == id)


def get_tag_by_id(db: Session, id: int) -> TagORM:
    return _get_tag_by_id(db, id).first()


def delete_tag(db: Session, id: int):
    _get_tag_by_id(db, id).delete()
    db.commit()


def update_tag(db: Session, id: int, new_tag: Tag):
    old_tag = get_tag_by_id(db, id)
    if old_tag.nome == new_tag.name:
        raise ValueError('No update')

    old_tag.nome = new_tag.name
    db.commit()
    db.refresh(old_tag)
    return old_tag