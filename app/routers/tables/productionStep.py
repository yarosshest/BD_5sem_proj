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
    prefix="/productionStep",
    tags=["productionStep"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_productionStep_page(request: Request, db: Db = Depends(db_ins)):
    productionStep = await db.get_production_step()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["data_time", "log", "id_equipment", "id_brewer"],
        "colRu": ["Дата и время", "Лог", "Оборудование", "Пивовар"],
        "colId": "id_production_step",
        "colIdRu": "id производственного шага",
        "items": productionStep,
        "name": "productionStep"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_productionStep(data_time: Annotated[str, Form()],
                             log: Annotated[str, Form()],
                             id_equipment: Annotated[int, Form()],
                             id_brewer: Annotated[int, Form()],
                             db: Db = Depends(db_ins)):
    await db.add_production_step(data_time, log, id_equipment, id_brewer)

    return "/web/productionStep"


@router.post("/dell/{id_production_step}", response_class=RedirectResponse, status_code=302)
async def dell_productionStep(id_production_step: int,
                              db: Db = Depends(db_ins)):
    await db.dell_production_step(id_production_step)

    return "/web/productionStep"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_productionStep(
        id: Annotated[int, Form()],
        data_time: Annotated[str, Form()],
        log: Annotated[str, Form()],
        id_equipment: Annotated[int, Form()],
        id_brewer: Annotated[int, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_production_step(id, data_time, log, id_equipment, id_brewer)

    return "/web/productionStep"


@router.get("/find", response_class=HTMLResponse)
async def find_productionStep(
        request: Request,
        id: str,
        data_time: str,
        log: str,
        id_equipment: str,
        id_brewer: str,
        db: Db = Depends(db_ins)):
    productionSteps = await db.get_production_step()
    res = []

    for productionStep in productionSteps:
        if (id != "" and id == str(productionStep.id_production_step)) or \
                (data_time != "" and data_time in str(productionStep.data_time)) or \
                (log != "" and log in productionStep.log) or \
                (id_equipment != "" and id_equipment == str(productionStep.id_equipment)) or \
                (id_brewer != "" and id_brewer == str(productionStep.id_brewer)):
            res.append(productionStep)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["data_time", "log", "id_equipment", "id_brewer"],
        "colRu": ["Дата и время", "Лог", "Оборудование", "Пивовар"],
        "colId": "id_production_step",
        "colIdRu": "id производственного шага",
        "items": res,
        "name": "productionStep"
    })
