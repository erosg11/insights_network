from typing import TypeVar

from fastapi import HTTPException
from fastapi import status

T = TypeVar('T')


def check_if_ok_or_raise_404(data: T, expected_class: str) -> T:
    if T is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'{expected_class} not found')
    return T
