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
    prefix="/productionSheet",
    tags=["productionSheet"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_productionSheet_page(request: Request, db: Db = Depends(db_ins)):
    productionSheet = await db.get_ProductionSheets()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name", "id_production_status", "id_request"],
        "colRu": ["Название", "Статус", "Заявка"],
        "colId": "id_production_sheet",
        "colIdRu": "id листа производства",
        "items": productionSheet,
        "name": "productionSheet"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_requestStatus(name: Annotated[str, Form()],
                            id_production_status: Annotated[int, Form()],
                            request_id: Annotated[int, Form()],
                            db: Db = Depends(db_ins)):
    await db.add_ProductionSheet(name, id_production_status, request_id)

    return "/web/productionSheet"

@router.post("/dell/{id_production_sheet}", response_class=RedirectResponse, status_code=302)
async def dell_requestStatus(id_production_sheet: int,
                             db: Db = Depends(db_ins)):
    await db.dell_ProductionSheet(id_production_sheet)

    return "/web/productionSheet"

@router.get("/find", response_class=HTMLResponse)
async def find_requestStatus(
        request: Request,
        id: str,
        name: str,
        id_production_status: str,
        id_request: str,
        db: Db = Depends(db_ins)):
    requestStatuses = await db.get_ProductionSheets()
    res = []

    for requestStatus in requestStatuses:
        if id != "" and str(requestStatus.id_production_sheet) == id:
            res.append(requestStatus)
        elif name != "" and requestStatus.name == name:
            res.append(requestStatus)
        elif id_production_status != "" and str(requestStatus.id_production_status) == id_production_status:
            res.append(requestStatus)
        elif id_request != "" and str(requestStatus.id_request) == id_request:
            res.append(requestStatus)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name", "id_production_status", "request_id"],
        "colRu": ["Название", "Статус", "Заявка"],
        "colId": "id_production_sheet",
        "colIdRu": "id листа производства",
        "items": res,
        "name": "productionSheet"
    })

