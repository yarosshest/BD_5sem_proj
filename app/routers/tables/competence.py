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
    prefix="/competence",
    tags=["competence"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_competence_page(request: Request, db: Db = Depends(db_ins)):
    competence = await db.get_competences()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name"],
        "colRu": ["Название"],
        "colId": "id_competence",
        "colIdRu": "id компетенции",
        "items": competence,
        "name": "competence"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_competence(name: Annotated[str, Form()],
                         db: Db = Depends(db_ins)):
    await db.add_competence(name)

    return "/web/competence"

@router.post("/dell/{id_competence}", response_class=RedirectResponse, status_code=302)
async def dell_competence(id_competence: int,
                          db: Db = Depends(db_ins)):
    await db.dell_competence(id_competence)

    return "/web/competence"

@router.get("/find", response_class=HTMLResponse)
async def find_competence(
        request: Request,
        id: str,
        name: str,
        db: Db = Depends(db_ins)):
    competence = await db.get_competences()
    res = []

    for competence in competence:
        if (id != "" and id == str(competence.id_competence)) or \
                (name != "" and name in competence.name):
            res.append(competence)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["name"],
        "colRu": ["Название"],
        "colId": "id_competence",
        "colIdRu": "id компетенции",
        "items": res,
        "name": "competence"
    })
