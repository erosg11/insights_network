from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.responses import Response
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from crud import get_tag_by_id, update_tag, delete_tag, create_tag
from dependencies import get_db, check_if_ok_or_raise_404
from entitys import Tag

router = APIRouter()


@router.get('/tag_id', response_model=Tag)
def get_tag(tag_id: int, db=Depends(get_db)):
    """Rota para obter uma tag pelo id"""
    return check_if_ok_or_raise_404(get_tag_by_id(db, tag_id), 'Tag')


@router.put('/{tag_id}', response_model=Tag)
def update_a_tag(tag_id: int, new_tag: Tag, db: Session = Depends(get_db)):
    """Rota para atualizar uma tag pelo id"""
    try:
        return update_tag(db, tag_id, new_tag)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Tag not found') from e


@router.delete('/{tag_id}', response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def delete_an_insight(tag_id: int, db: Session = Depends(get_db)):
    """Rota para deletar uma tag pelo id"""
    delete_tag(db, tag_id)


@router.post('/', response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_new_insight(new_tag: str, db: Session = Depends(get_db)):
    return create_tag(db, new_tag)
