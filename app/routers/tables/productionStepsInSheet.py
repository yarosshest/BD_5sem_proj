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
    prefix="/productionStepsInSheet",
    tags=["productionStepsInSheet"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_productionStepsInSheet_page(request: Request, db: Db = Depends(db_ins)):
    productionStepsInSheet = await db.get_production_steps_in_sheet()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["id_production_sheet", "id_production_step"],
        "colRu": ["Производственный лист", "Производственный шаг"],
        "colId": "id_production_steps_in_sheet",
        "colIdRu": "id производственного шага в листе",
        "items": productionStepsInSheet,
        "name": "productionStepsInSheet"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_productionStepsInSheet(id_production_sheet: Annotated[int, Form()],
                                     id_production_step: Annotated[int, Form()],
                                     db: Db = Depends(db_ins)):
    await db.add_production_steps_in_sheet(id_production_sheet, id_production_step)

    return "/web/productionStepsInSheet"


@router.post("/dell/{id_production_step_in_sheet}", response_class=RedirectResponse, status_code=302)
async def dell_productionStepsInSheet(id_production_step_in_sheet: int,
                                      db: Db = Depends(db_ins)):
    await db.dell_production_steps_in_sheet(id_production_step_in_sheet)

    return "/web/productionStepsInSheet"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_productionStepsInSheet(
        id: Annotated[int, Form()],
        id_production_sheet: Annotated[int, Form()],
        id_production_step: Annotated[int, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_production_steps_in_sheet(id, id_production_sheet, id_production_step)

    return "/web/productionStepsInSheet"


@router.get("/find", response_class=HTMLResponse)
async def find_productionStepsInSheet(
        request: Request,
        id_production_sheet: str,
        id_production_step: str,
        db: Db = Depends(db_ins)):
    productionStepsInSheet = await db.get_production_steps_in_sheet()
    result = []

    for productionStepInSheet in productionStepsInSheet:
        if str(productionStepInSheet.id_production_sheet) == id_production_sheet and \
                str(productionStepInSheet.id_production_step) == id_production_step:
            result.append(productionStepInSheet)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["id_production_sheet", "id_production_step"],
        "colRu": ["Производственный лист", "Производственный шаг"],
        "colId": "id_production_steps_in_sheet",
        "colIdRu": "id производственного шага в листе",
        "items": result,
        "name": "productionStepsInSheet"
    })
