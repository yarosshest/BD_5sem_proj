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

from pathlib import Path

router = APIRouter(
    prefix="/web",
    tags=["web"],

)

script_dir = Path(__file__).parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("home_page.html", {
        "request": request,
    })


@router.get("/clients", response_class=HTMLResponse)
async def get_client_page(request: Request, db: Db = Depends(db_ins)):
    clients = await db.get_clients()

    return templates.TemplateResponse("client_page.html", {
        "request": request,
        "col": ["id клиента", "ФИО", "ИНН", "Телефон"],
        "clients": clients
    })


@router.post("/client/add", response_class=RedirectResponse, status_code=302)
async def add_client(fio: Annotated[str, Form()],
                     inn: Annotated[str, Form()],
                     phone: Annotated[str, Form()],
                     db: Db = Depends(db_ins)):
    await db.add_client(fio, inn, phone)

    return "/web/clients"


@router.post("/dell/client/{id_client}", response_class=RedirectResponse, status_code=302)
async def dell_client(id_client: int,
                      db: Db = Depends(db_ins)):
    await db.dell_client(id_client)

    return "/web/clients"


@router.post("/client/edit", response_class=RedirectResponse, status_code=302)
async def edit_client(
        id: Annotated[int, Form()],
        fio: Annotated[str, Form()],
        inn: Annotated[str, Form()],
        phone: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_client(id, fio, inn, phone)

    return "/web/clients"


@router.get("/lawyer", response_class=HTMLResponse)
async def get_client_page(request: Request, db: Db = Depends(db_ins)):
    lawyers = await db.get_lawyers()

    return templates.TemplateResponse("lawyer_page.html", {
        "request": request,
        "col": ["id_lawyer", "FIO", "salary"],
        "colRu": ["id клиента", "ФИО", "Зарплата"],
        "items": lawyers
    })


@router.post("/client/add", response_class=RedirectResponse, status_code=302)
async def add_client(fio: Annotated[str, Form()],
                     inn: Annotated[str, Form()],
                     phone: Annotated[str, Form()],
                     db: Db = Depends(db_ins)):
    await db.add_client(fio, inn, phone)

    return "/web/clients"


@router.post("/dell/client/{id_client}", response_class=RedirectResponse, status_code=302)
async def dell_client(id_client: int,
                      db: Db = Depends(db_ins)):
    await db.dell_client(id_client)

    return "/web/clients"


@router.post("/client/edit", response_class=RedirectResponse, status_code=302)
async def edit_client(
        id: Annotated[int, Form()],
        fio: Annotated[str, Form()],
        inn: Annotated[str, Form()],
        phone: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_client(id, fio, inn, phone)

    return "/web/clients"