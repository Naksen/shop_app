#!/bin/bash

alembic upgrade head

cd src

uvicorn main:app --reload --host 0.0.0.0 --port 8000