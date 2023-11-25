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
    prefix="/contractStatus",
    tags=["contractStatus"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_contractStatus_page(request: Request, db: Db = Depends(db_ins)):
    contractStatuses = await db.get_contractStatuses()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_contract_status",
        "colIdRu": "id статуса",
        "items": contractStatuses,
        "name": "contractStatus"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_contractStatus(status: Annotated[str, Form()],
                             db: Db = Depends(db_ins)):
    await db.add_contractStatus(status)

    return "/web/contractStatus"

@router.post("/dell/{id_contractStatus}", response_class=RedirectResponse, status_code=302)
async def dell_contractStatus(id_contractStatus: int,
                              db: Db = Depends(db_ins)):
    await db.dell_contractStatus(id_contractStatus)

    return "/web/contractStatus"

@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_contractStatus(
        id: Annotated[int, Form()],
        status: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_contractStatus(id, status)

    return "/web/contractStatus"

@router.get("/find", response_class=HTMLResponse)
async def find_contractStatus(
        request: Request,
        id: str,
        status: str,
        db: Db = Depends(db_ins)):
    contractStatuses = await db.get_contractStatuses()
    res = []

    for contractStatus in contractStatuses:
        if contractStatus.id_contract_status == int(id) or( status in contractStatus.status and status != ""):
            res.append(contractStatus)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_contract_status",
        "colIdRu": "id статуса",
        "items": res,
        "name": "contractStatus"
    })

