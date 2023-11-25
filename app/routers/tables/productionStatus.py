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
    prefix="/productionStatus",
    tags=["productionStatus"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_productionStatus_page(request: Request, db: Db = Depends(db_ins)):
    productionStatus = await db.get_ProductionStatuses()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_production_status",
        "colIdRu": "id статуса",
        "items": productionStatus,
        "name": "productionStatus"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_requestStatus(status: Annotated[str, Form()],
                            db: Db = Depends(db_ins)):
    await db.add_ProductionStatus(status)

    return "/web/productionStatus"

@router.post("/dell/{id_production_status}", response_class=RedirectResponse, status_code=302)
async def dell_requestStatus(id_production_status: int,
                             db: Db = Depends(db_ins)):
    await db.dell_ProductionStatus(id_production_status)

    return "/web/productionStatus"

@router.get("/find", response_class=HTMLResponse)
async def find_requestStatus(
        request: Request,
        id: str,
        status: str,
        db: Db = Depends(db_ins)):
    requestStatuses = await db.get_ProductionStatuses()
    res = []


    for requestStatus in requestStatuses:
        if id != "" and str(requestStatus.id_production_status) == id:
            res.append(requestStatus)
        if status != "" and status in requestStatus.status:
            res.append(requestStatus)


    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_production_status",
        "colIdRu": "id статуса",
        "items": res,
        "name": "productionStatus"
    })
