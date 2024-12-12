from fastapi import FastAPI, APIRouter
from api_v1.views import router_questionnaire_admin, router_admin, router_questionnaire_user
import uvicorn

app = FastAPI(title='Проект Опросник')

router = APIRouter()

router.include_router(router_admin)
router.include_router(router_questionnaire_user)
router.include_router(router_questionnaire_admin)

app.include_router(router)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)