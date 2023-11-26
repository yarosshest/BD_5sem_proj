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
    prefix="/brewer",
    tags=["brewer"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_brewer_page(request: Request, db: Db = Depends(db_ins)):
    brewers = await db.get_brewers()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["FIO", "salary", "id_competence"],
        "colRu": ["ФИО", "Зарплата", "Компетенция"],
        "colId": "id_brewer",
        "colIdRu": "id пивовара",
        "items": brewers,
        "name": "brewer"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_brewer(FIO: Annotated[str, Form()],
                     salary: Annotated[int, Form()],
                     id_competence: Annotated[int, Form()],
                     db: Db = Depends(db_ins)):
    await db.add_brewer(FIO, salary, id_competence)

    return "/web/brewer"


@router.post("/dell/{id_brewer}", response_class=RedirectResponse, status_code=302)
async def dell_brewer(id_brewer: int,
                      db: Db = Depends(db_ins)):
    await db.dell_brewer(id_brewer)

    return "/web/brewer"

@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_brewer(
        id: Annotated[int, Form()],
        FIO: Annotated[str, Form()],
        salary: Annotated[int, Form()],
        id_competence: Annotated[int, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_brewer(id, FIO, salary, id_competence)

    return "/web/brewer"

@router.get("/find", response_class=HTMLResponse)
async def find_brewer(
        request: Request,
        id: str,
        FIO: str,
        salary: str,
        id_competence: str,
        db: Db = Depends(db_ins)):
    brewers = await db.get_brewers()
    res = []

    for brewer in brewers:
        if (id != "" and id == str(brewer.id_brewer)) or \
                (FIO != "" and FIO in brewer.FIO) or \
                (salary != "" and salary in str(brewer.salary)) or \
                (id_competence != "" and id_competence == str(brewer.id_competence)):
            res.append(brewer)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["FIO", "salary", "id_competence"],
        "colRu": ["ФИО", "Зарплата", "Компетенция"],
        "colId": "id_brewer",
        "colIdRu": "id пивовара",
        "items": res,
        "name": "brewer"
    })