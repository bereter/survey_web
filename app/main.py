from fastapi import FastAPI, APIRouter
from api_v1.views import router_questionnaire, router_admin
import uvicorn

app = FastAPI()

router = APIRouter()

router.include_router(router_admin)
router.include_router(router_questionnaire)

app.include_router(router)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)