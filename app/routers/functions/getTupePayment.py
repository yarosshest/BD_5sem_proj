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
    prefix="/getTupePayment",
    tags=["getTupePayment"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_tupe_payment_page(request: Request):
    return templates.TemplateResponse("get_tupe_payment_page.html", {
        "request": request,
        "has_result": False,
    })


@router.post("/cal", response_class=HTMLResponse)
async def cal_get_tupe_payment_page(
        request: Request,
        id: Annotated[int, Form()],
        db: Db = Depends(db_ins)
):
    status = await db.get_tupe_payment(id)
    return templates.TemplateResponse("get_tupe_payment_page.html", {
        "request": request,
        "has_result": True,
        "status": status
    })
