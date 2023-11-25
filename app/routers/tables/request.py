from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from database.async_db import DataBase as Db
from database.async_db import db as db_ins

router = APIRouter(
    prefix="/request",
    tags=["request"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_request_page(request: Request, db: Db = Depends(db_ins)):
    requests = await db.get_requests()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["id_client", "id_lawyer", "id_payment", "id_contract", "id_request_status"],
        "colRu": ["Клиент", "Юрист", "Оплата", "Контракт", "Статус"],
        "colId": "id_request",
        "colIdRu": "id заявки",
        "items": requests,
        "name": "request"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_request(id_client: Annotated[int, Form()],
                      id_lawyer: Annotated[int, Form()],
                      id_payment: Annotated[int, Form()],
                      id_contract: Annotated[int, Form()],
                      id_request_status: Annotated[int, Form()],
                      db: Db = Depends(db_ins)):
    await db.add_request(id_client, id_lawyer, id_payment, id_contract, id_request_status)

    return "/web/request"


@router.post("/dell/{id_request}", response_class=RedirectResponse, status_code=302)
async def dell_request(id_request: int,
                       db: Db = Depends(db_ins)):
    await db.dell_request(id_request)

    return "/web/request"


@router.get("/find", response_class=HTMLResponse)
async def find_request(
        re: Request,
        id: str,
        id_client: str,
        id_lawyer: str,
        id_payment: str,
        id_contract: str,
        id_request_status: str,
        db: Db = Depends(db_ins)):
    requests = await db.get_requests()
    res = []

    for request in requests:
        if id != "" and str(request.id_request) == id:
            res.append(request)
        if id_client != "" and str(request.id_client) == id_client:
            res.append(request)
        if id_lawyer != "" and str(request.id_lawyer) == id_lawyer:
            res.append(request)
        if id_payment != "" and str(request.id_payment) == id_payment:
            res.append(request)
        if id_contract != "" and str(request.id_contract) == id_contract:
            res.append(request)
        if id_request_status != "" and str(request.id_request_status) == id_request_status:
            res.append(request)

    return templates.TemplateResponse("table_page.html", {
        "request": re,
        "col": ["id_client", "id_lawyer", "id_payment", "id_contract", "id_request_status"],
        "colRu": ["Клиент", "Юрист", "Оплата", "Контракт", "Статус"],
        "colId": "id_request",
        "colIdRu": "id заявки",
        "items": res,
        "name": "request"
    })
