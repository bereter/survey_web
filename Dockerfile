FROM python:3.12

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/backend"
# WORKDIR app
# CMD gunicorn main:main_app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000