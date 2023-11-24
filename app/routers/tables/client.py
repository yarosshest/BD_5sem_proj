import os
from datetime import timedelta, datetime
from pathlib import Path
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

router = APIRouter(
    prefix="/client",
    tags=["client"],

)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_client_page(request: Request, db: Db = Depends(db_ins)):
    clients = await db.get_clients()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["FIO", "INN", "phone"],
        "colRu": ["ФИО", "ИНН", "Телефон"],
        "colId": "id_client",
        "colIdRu": "id клиента",
        "items": clients,
        "name": "client"
    })


@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_client(FIO: Annotated[str, Form()],
                     INN: Annotated[str, Form()],
                     phone: Annotated[str, Form()],
                     db: Db = Depends(db_ins)):
    await db.add_client(FIO, INN, phone)

    return "/web/client"


@router.post("/dell/{id_client}", response_class=RedirectResponse, status_code=302)
async def dell_client(id_client: int,
                      db: Db = Depends(db_ins)):
    await db.dell_client(id_client)

    return "/web/client"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_client(
        id: Annotated[int, Form()],
        FIO: Annotated[str, Form()],
        INN: Annotated[str, Form()],
        phone: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_client(id, FIO, INN, phone)

    return "/web/client"


@router.post("/find", response_class=HTMLResponse)
async def find_client(request: Request,
                      id: Annotated[str, Form()],
                      FIO: Annotated[str, Form()],
                      INN: Annotated[str, Form()],
                      phone: Annotated[str, Form()],
                      db: Db = Depends(db_ins)):
    clients = await db.get_clients()
    res = []

    if id != '':
        for d in clients:
            if id in str(d.id_client):
                res.append(d)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["FIO", "INN", "phone"],
        "colRu": ["ФИО", "ИНН", "Телефон"],
        "colId": "id_client",
        "colIdRu": "id клиента",
        "items": res,
        "name": "client"
    })
