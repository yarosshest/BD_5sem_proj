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
    prefix="/contract",
    tags=["contract"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_contract_page(request: Request, db: Db = Depends(db_ins)):
    contracts = await db.get_contracts()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["link", "id_contract_status"],
        "colRu": ["ссылка", "id статуса"],
        "colId": "id_contract",
        "colIdRu": "id контракта",
        "items": contracts,
        "name": "contract"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_contract(link: Annotated[str, Form()],
                       id_contract_status: Annotated[str, Form()],
                       db: Db = Depends(db_ins)):
    await db.add_contract(link, int(id_contract_status))

    return "/web/contract"

@router.post("/dell/{id_contract}", response_class=RedirectResponse, status_code=302)
async def dell_contract(id_contract: int,
                        db: Db = Depends(db_ins)):
    await db.dell_contract(id_contract)

    return "/web/contract"

@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_contract(
        id: Annotated[int, Form()],
        link: Annotated[str, Form()],
        id_contract_status: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_contract(id, link, int(id_contract_status))

    return "/web/contract"

@router.get("/find", response_class=HTMLResponse)
async def find_contract(
        request: Request,
        id: str,
        link: str,
        id_contract_status: str,
        db: Db = Depends(db_ins)):
    contracts = await db.get_contracts()
    res = []

    for contract in contracts:
        if contract.id_contract == id or link in contract.link or contract.id_contract_status == id_contract_status:
            res.append(contract)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["link", "id_contract_status"],
        "colRu": ["ссылка", "id статуса"],
        "colId": "id_contract",
        "colIdRu": "id контракта",
        "items": res,
        "name": "contract"
    })