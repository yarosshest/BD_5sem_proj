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
    prefix="/spoilage",
    tags=["spoilage"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_spoilage_page(request: Request, db: Db = Depends(db_ins)):
    spoilage = await db.get_spoilage()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["id_spoilage", "amount", "item", "id_production_sheet"],
        "colRu": ["id брака", "Количество", "Предмет", "Производственный лист"],
        "colId": "id_spoilage",
        "colIdRu": "id брака",
        "items": spoilage,
        "name": "spoilage"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_spoilage(amount: Annotated[str, Form()],
                       item: Annotated[str, Form()],
                       id_production_sheet: Annotated[int, Form()],
                       db: Db = Depends(db_ins)):
    await db.add_spoilage(amount, item, id_production_sheet)

    return "/web/spoilage"


@router.post("/dell/{id_spoilage}", response_class=RedirectResponse, status_code=302)
async def dell_spoilage(id_spoilage: int,
                        db: Db = Depends(db_ins)):
    await db.dell_spoilage(id_spoilage)

    return "/web/spoilage"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_spoilage(
        id: Annotated[int, Form()],
        amount: Annotated[str, Form()],
        item: Annotated[str, Form()],
        id_production_sheet: Annotated[int, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_spoilage(id, amount, item, id_production_sheet)

    return "/web/spoilage"


@router.get("/search", response_class=HTMLResponse)
async def search_spoilage(request: Request,
                          id_spoilage: str = 0,
                          amount: str = "",
                          item: str = "",
                          id_production_sheet: str = 0,
                          db: Db = Depends(db_ins)):
    spoilage = await db.get_spoilage()
    res = []

    for i in spoilage:
        if (id_spoilage != "" or str(i.id_spoilage) == id_spoilage) and \
                (amount != "" or amount in i.amount) and \
                (item != "" or item == i.item) and \
                (id_production_sheet != "" or i.id_production_sheet == id_production_sheet):
            res.append(i)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["id_spoilage", "amount", "item", "id_production_sheet"],
        "colRu": ["id брака", "Количество", "Предмет", "Производственный лист"],
        "colId": "id_spoilage",
        "colIdRu": "id брака",
        "items": res,
        "name": "spoilage"
    })
