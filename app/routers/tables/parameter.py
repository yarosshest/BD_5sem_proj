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
    prefix="/parameter",
    tags=["parameter"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_parameter_page(request: Request, db: Db = Depends(db_ins)):
    parameters = await db.get_parameters()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name"],
        "colRu": ["Название"],
        "colId": "id_parameter",
        "colIdRu": "id параметра",
        "items": parameters,
        "name": "parameter"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_parameter(name: Annotated[str, Form()],
                        db: Db = Depends(db_ins)):
    await db.add_parameter(name)

    return "/web/parameter"

@router.post("/dell/{id_parameter}", response_class=RedirectResponse, status_code=302)
async def dell_parameter(id_parameter: int,
                         db: Db = Depends(db_ins)):
    await db.dell_parameter(id_parameter)

    return "/web/parameter"

@router.get("/find", response_class=HTMLResponse)
async def find_parameter(
        request: Request,
        id: str,
        name: str,
        db: Db = Depends(db_ins)):
    parameters = await db.get_parameters()
    res = []

    for parameter in parameters:
        if (id != "" and id == str(parameter.id_parameter)) or \
                (name != "" and name in parameter.name):
            res.append(parameter)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name"],
        "colRu": ["Название"],
        "colId": "id_parameter",
        "colIdRu": "id параметра",
        "items": res,
        "name": "parameter"
    })


