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
    prefix="/lawyer",
    tags=["lawyer"],

)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_lawyer_page(request: Request, db: Db = Depends(db_ins)):
    lawyers = await db.get_lawyers()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["FIO", "salary"],
        "colRu": ["ФИО", "Зарплата"],
        "colId": "id_lawyer",
        "colIdRu": "id юриста",
        "items": lawyers,
        "name": "lawyer"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_lawyer(FIO: Annotated[str, Form()],
                     salary: Annotated[str, Form()],
                     db: Db = Depends(db_ins)):
    await db.add_lawyer(FIO, salary)

    return "/web/lawyer"


@router.post("/dell/{id_lawyer}", response_class=RedirectResponse, status_code=302)
async def dell_lawyer(id_lawyer: int,
                      db: Db = Depends(db_ins)):
    await db.dell_lawyer(id_lawyer)

    return "/web/lawyer"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_lawyer(
        id: Annotated[int, Form()],
        FIO: Annotated[str, Form()],
        salary: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_lawyer(id, FIO, salary)

    return "/web/lawyer"


@router.get("/find", response_class=HTMLResponse)
async def find_lawyer(request: Request,
                      id: str,
                      FIO: str,
                      salary: str,
                      db: Db = Depends(db_ins)):
    lawyers = await db.get_lawyers()
    res = []

    for l in lawyers:
        if id is not "":
            if id in l.id_lawyer and l not in res:
                res.append(l)
        if FIO is not "":
            if FIO in l.FIO and l not in res:
                res.append(l)
        if salary is not "":
            if salary in l.salary and l not in res:
                res.append(l)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["FIO", "salary"],
        "colRu": ["ФИО", "Зарплата"],
        "colId": "id_lawyer",
        "colIdRu": "id юриста",
        "items": res,
        "name": "lawyer"
    })

