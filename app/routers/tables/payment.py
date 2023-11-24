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
    prefix="/payment",
    tags=["payment"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_payment_page(request: Request, db: Db = Depends(db_ins)):
    payments = await db.get_payments()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["amount", "id_lawyer", "id_payment_status", "sum"],
        "colRu": ["id клиента", "id юриста", "id статуса", "Сумма"],
        "colId": "id_payment",
        "colIdRu": "id платежа",
        "items": payments,
        "name": "payment"
    })