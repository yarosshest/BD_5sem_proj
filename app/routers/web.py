from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.routers.tables.client import router as client
from app.routers.tables.lawyer import router as lawyer
from app.routers.tables.paymentStatus import router as paymentStatus
from app.routers.tables.payment import router as payment
from app.routers.tables.contractStatus import router as contractStatus
from app.routers.tables.contract import router as contract
from app.routers.tables.requestStatus import router as requestStatus
from app.routers.tables.request import router as request
from app.routers.tables.productionStatus import router as productionStatus
from app.routers.tables.productionSheet import router as productionSheet
from app.routers.tables.competence import router as competence
from app.routers.tables.brewer import router as brewer
from app.routers.tables.parameter import router as parameter
from app.routers.tables.equipmentParameters import router as equipmentParameters
from app.routers.tables.equipment import router as equipment
from app.routers.tables.productionStep import router as productionStep
from app.routers.tables.spoilage import router as spoilage
from app.routers.tables.productionStepsInSheet import router as productionStepsInSheet

from pathlib import Path

router = APIRouter(
    prefix="/web",
    tags=["web"],
)

router.include_router(client)
router.include_router(lawyer)
router.include_router(paymentStatus)
router.include_router(payment)
router.include_router(contractStatus)
router.include_router(contract)
router.include_router(requestStatus)
router.include_router(request)
router.include_router(productionStatus)
router.include_router(productionSheet)
router.include_router(competence)
router.include_router(brewer)
router.include_router(parameter)
router.include_router(equipmentParameters)
router.include_router(equipment)
router.include_router(productionStep)
router.include_router(spoilage)
router.include_router(productionStepsInSheet)

script_dir = Path(__file__).parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


@router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("home_page.html", {
        "request": request,
    })
