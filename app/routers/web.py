from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.routers.tables.client import router as client
from app.routers.tables.lawyer import router as lawyer
from app.routers.tables.paymentStatus import router as paymentStatus

from pathlib import Path

router = APIRouter(
    prefix="/web",
    tags=["web"],
)

router.include_router(client)
router.include_router(lawyer)
router.include_router(paymentStatus)


script_dir = Path(__file__).parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("home_page.html", {
        "request": request,
    })