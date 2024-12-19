from fastapi import APIRouter
from .router_user import router_questionnaire_user
from .router_admin import router_questionnaire_admin
from .router_auth import router_admin

router = APIRouter()

router.include_router(router=router_admin)
router.include_router(router=router_questionnaire_admin)
router.include_router(router=router_questionnaire_user)

