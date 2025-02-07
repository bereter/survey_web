from fastapi import FastAPI, APIRouter
from api_v1 import router
import uvicorn

app = FastAPI(title='Проект Опросник')


app.include_router(router)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)