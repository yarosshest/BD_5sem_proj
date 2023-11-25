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
    prefix="/requestStatus",
    tags=["requestStatus"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)

@router.get("/", response_class=HTMLResponse)
async def get_requestStatus_page(request: Request, db: Db = Depends(db_ins)):
    requestStatuses = await db.get_requestStatuses()

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_request_status",
        "colIdRu": "id статуса",
        "items": requestStatuses,
        "name": "requestStatus"
    })

@router.post("/add", response_class=RedirectResponse, status_code=302)
async def add_requestStatus(status: Annotated[str, Form()],
                            db: Db = Depends(db_ins)):
    await db.add_requestStatus(status)

    return "/web/requestStatus"

@router.post("/dell/{id_requestStatus}", response_class=RedirectResponse, status_code=302)
async def dell_requestStatus(id_requestStatus: int,
                             db: Db = Depends(db_ins)):
    await db.dell_requestStatus(id_requestStatus)

    return "/web/requestStatus"


@router.post("/edit", response_class=RedirectResponse, status_code=302)
async def edit_requestStatus(
        id: Annotated[int, Form()],
        status: Annotated[str, Form()],
        db: Db = Depends(db_ins)):
    await db.edit_requestStatus(id, status)

    return "/web/requestStatus"

@router.get("/find", response_class=HTMLResponse)
async def find_requestStatus(
        request: Request,
        id: str,
        status: str,
        db: Db = Depends(db_ins)):
    requestStatuses = await db.get_requestStatuses()

    res = []

    for requestStatus in requestStatuses:
        if requestStatus.id_request_status == int(id) or( status in requestStatus.status and status != ""):
            res.append(requestStatus)

    return templates.TemplateResponse("table_page.html", {
        "request": request,
        "col": ["status"],
        "colRu": ["Статус"],
        "colId": "id_request_status",
        "colIdRu": "id статуса",
        "items": res,
        "name": "requestStatus"
    })