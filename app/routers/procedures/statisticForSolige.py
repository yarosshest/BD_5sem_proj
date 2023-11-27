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
    prefix="/statisticForSolige",
    tags=["statisticForSolige"],
)

script_dir = Path(__file__).parent.parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_call_statistic_for_solige(request: Request, db: Db = Depends(db_ins)):
    res = await db.call_statistic_for_solige()
    return templates.TemplateResponse("call_statistic_for_solige.html", {
        "request": request,
        "items": res,
    })