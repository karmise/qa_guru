from http import HTTPStatus

from fastapi import APIRouter

from homework_1.app.database.engine import check_availability
from homework_1.app.models.AppStatus import AppStatus


router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_availability())