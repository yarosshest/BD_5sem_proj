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
    prefix="/paymentStatus",
    tags=["paymentStatus"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_paymentStatus_page(request: Request, db: Db = Depends(db_ins)):
    paymentStatuses = await db.get_paymentStatuses()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_payment_status",
        "colIdRu": "id статуса",
        "items": paymentStatuses,
        "name": "paymentStatus"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_paymentStatus(status: Annotated[str, Form()],
                            db: Db = Depends(db_ins)):
    await db.add_paymentStatus(status)

    return "/web/paymentStatus"


@router.post("/dell/{id_paymentStatus}", response_class=RedirectResponse, status_code=302)
async def dell_paymentStatus(id_paymentStatus: int,
                             db: Db = Depends(db_ins)):
    await db.dell_paymentStatus(id_paymentStatus)

    return "/web/paymentStatus"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_paymentStatus(
        id: Annotated[int, Form()],
        status: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_paymentStatus(id, status)

    return "/web/paymentStatus"


@router.get("/find", response_class=HTMLResponse)
async def find_paymentStatus(request: Request,
                             id: str,
                             status: str,
                             db: Db = Depends(db_ins)):
    paymentStatuses = await db.get_paymentStatuses()
    res = []

    for p in paymentStatuses:
        if id != "" and id in str(p.id_payment_status):
            res.append(p)
        if status != "" and status in p.status:
            res.append(p)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_payment_status",
        "colIdRu": "id статуса",
        "items": res,
        "name": "paymentStatus"
    })
