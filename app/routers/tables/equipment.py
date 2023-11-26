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
    prefix="/equipment",
    tags=["equipment"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_equipment_page(request: Request, db: Db = Depends(db_ins)):
    equipment = await db.get_equipment()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name", "resource"],
        "colRu": ["Название", "Ресурс"],
        "colId": "id_equipment",
        "colIdRu": "id оборудования",
        "items": equipment,
        "name": "equipment"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_equipment(name: Annotated[str, Form()],
                        resource: Annotated[str, Form()],
                        db: Db = Depends(db_ins)):
    await db.add_equipment(name, resource)

    return "/web/equipment"


@router.post("/dell/{id_equipment}", response_class=RedirectResponse, status_code=302)
async def dell_equipment(id_equipment: int,
                         db: Db = Depends(db_ins)):
    await db.dell_equipment(id_equipment)

    return "/web/equipment"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_equipment(
        id: Annotated[int, Form()],
        name: Annotated[str, Form()],
        resource: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_equipment(id, name, resource)

    return "/web/equipment"


@router.get("/find", response_class=HTMLResponse)
async def find_equipment(request: Request,
                         id: str,
                         name: str,
                         resource: str,
                         db: Db = Depends(db_ins)):
    equipment = await db.get_equipment()
    res = []

    for i in equipment:
        if (id != "" and str(i.id_equipment) == id) or (name != "" and name in i.name) or (
                resource != "" and resource in i.resource):
            res.append(i)


    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name", "resource"],
        "colRu": ["Название", "Ресурс"],
        "colId": "id_equipment",
        "colIdRu": "id оборудования",
        "items": res,
        "name": "equipment"
    })
