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
    prefix="/equipmentParameters",
    tags=["equipmentParameters"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_equipmentParameters_page(request: Request, db: Db = Depends(db_ins)):
    equipmentParameters = await db.get_equipment_parameters()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["id_equipment", "id_parameter"],
        "colRu": ["Оборудование", "Параметр"],
        "colId": "id_equipment_parameters",
        "colIdRu": "id параметра оборудования",
        "items": equipmentParameters,
        "name": "equipmentParameters"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_equipmentParameters(id_equipment: Annotated[int, Form()],
                                  id_parameter: Annotated[int, Form()],
                                  db: Db = Depends(db_ins)):
    await db.add_equipment_parameters(id_equipment, id_parameter)

    return "/web/equipmentParameters"

@router.post("/dell/{id_equipment_parameters}", response_class=RedirectResponse, status_code=302)
async def dell_equipmentParameters(id_equipment_parameters: int,
                                   db: Db = Depends(db_ins)):
    await db.dell_equipment_parameters(id_equipment_parameters)

    return "/web/equipmentParameters"

@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_equipmentParameters(
        id: Annotated[int, Form()],
        id_equipment: Annotated[int, Form()],
        id_parameter: Annotated[int, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_equipment_parameters(id, id_equipment, id_parameter)

    return "/web/equipmentParameters"

@router.get("/find", response_class=HTMLResponse)
async def find_equipmentParameters(
        request: Request,
        id: str,
        id_equipment: str,
        id_parameter: str,
        db: Db = Depends(db_ins)):
    equipmentParameters = await db.get_equipment_parameters()
    res = []

    for equipmentParameter in equipmentParameters:
        if (id != "" and id == str(equipmentParameter.id_equipment_parameters)) or \
                (id_equipment != "" and id_equipment == str(equipmentParameter.id_equipment)) or \
                (id_parameter != "" and id_parameter == str(equipmentParameter.id_parameter)):
            res.append(equipmentParameter)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["id_equipment", "id_parameter"],
        "colRu": ["Оборудование", "Параметр"],
        "colId": "id_equipment_parameters",
        "colIdRu": "id параметра оборудования",
        "items": res,
        "name": "equipmentParameters"
    })