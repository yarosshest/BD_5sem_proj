import os
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.models.Message import Message
from database.Db_objects import Client
from database.async_db import DataBase as Db
from database.async_db import db as db_ins
from app.routers.tables.client import router as client

from pathlib import Path

router = APIRouter(
    prefix="/web",
    tags=["web"],

)

router.include_router(client)

script_dir = Path(__file__).parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("home_page.html", {
        "request": request,
    })


@router.get("/lawyer", response_class=HTMLResponse)
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


@router.post("/lawyer/add", response_class=RedirectResponse, status_code=302)
async def add_lawyer(FIO: Annotated[str, Form()],
                     salary: Annotated[str, Form()],
                     db: Db = Depends(db_ins)):
    await db.add_lawyer(FIO, salary)

    return "/web/lawyer"


@router.post("/lawyer/dell/{id}", response_class=RedirectResponse, status_code=302)
async def dell_lawyer(id: int,
                      db: Db = Depends(db_ins)):
    await db.dell_lawyer(id)

    return "/web/lawyer"


@router.post("/lawyer/edit", response_class=RedirectResponse, status_code=302)
async def edit_lawyer(
        id: Annotated[int, Form()],
        FIO: Annotated[str, Form()],
        salary: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_lawyer(id, FIO, salary)

    return "/web/lawyer"
