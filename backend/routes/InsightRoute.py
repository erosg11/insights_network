from typing import Optional, List

from fastapi import Depends, Query, HTTPException
from fastapi import status
from fastapi.responses import Response
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from crud import get_insight_by_id, update_insight, delete_insight, create_insight, list_cards
from dependencies import get_db, check_if_ok_or_raise_404
from entitys import Insight, NewInsight, InsightList

router = APIRouter()


@router.get('/{insight_id}', response_model=Insight)
def read_insight(insight_id: int, db: Session = Depends(get_db)):
    """Rota para obter um insight por id"""
    return check_if_ok_or_raise_404(get_insight_by_id(db, insight_id), 'Insight')


@router.put('/{insight_id}', response_model=Insight)
def update_an_insight(insight_id: int, new_insight: NewInsight, db: Session = Depends(get_db)):
    """Rota para atualizar um insight pelo id"""
    try:
        return update_insight(db, insight_id, new_insight)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Insight not found') from e


@router.delete('/{insight_id}', response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def delete_an_insight(insight_id: int, db: Session = Depends(get_db)):
    """Rota para deletar insight pelo id"""
    delete_insight(db, insight_id)


@router.post('/', response_model=Insight, status_code=status.HTTP_201_CREATED)
def create_new_insight(new_insight: NewInsight, db: Session = Depends(get_db)):
    return create_insight(db, new_insight)


@router.get('/', response_model=InsightList)
def get_insights(tags: Optional[List[str]] = Query(None), db: Session = Depends(get_db), skip=0, limit=10):
    return InsightList(insights=list_cards(db, tags, skip, limit))
