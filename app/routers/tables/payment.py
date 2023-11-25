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
        "col": ["amount", "id_payment_status"],
        "colRu": ["Сумма", "id статуса"],
        "colId": "id_payment",
        "colIdRu": "id платежа",
        "items": payments,
        "name": "payment"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_payment(amount: Annotated[str, Form()],
                      id_payment_status: Annotated[str, Form()],
                      db: Db = Depends(db_ins)):
    await db.add_payment(amount, int(id_payment_status))

    return "/web/payment"


@router.post("/dell/{id_payment}", response_class=RedirectResponse, status_code=302)
async def dell_payment(id_payment: int,
                       db: Db = Depends(db_ins)):
    await db.dell_payment(id_payment)

    return "/web/payment"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_payment(
        id: Annotated[int, Form()],
        amount: Annotated[str, Form()],
        id_payment_status: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_payment(id, amount, int(id_payment_status))

    return "/web/payment"


@router.get("/find", response_class=RedirectResponse, status_code=302)
async def filter_payment(
        request: Request,
        amount: str,
        id_payment_status: str,
        db: Db = Depends(db_ins)):
    payments = await db.get_payments()

    res = []

    for payment in payments:
        if amount != "" and amount in str(payment.amount) and payment not in res:
            res.append(payment)
        if id_payment_status != "" and id_payment_status in str(payment.id_payment_status)and payment not in res:
            res.append(payment)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["amount", "id_payment_status"],
        "colRu": ["Сумма", "id статуса"],
        "colId": "id_payment",
        "colIdRu": "id платежа",
        "items": res,
        "name": "payment"
    })
