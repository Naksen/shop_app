FROM python:3.11

RUN pip install poetry

WORKDIR /fastapi_app

COPY pyproject.toml poetry.lock /fastapi_app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /fastapi_app/

RUN chmod a+x docker/*.sh

# WORKDIR /fastapi_app/src

# CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

