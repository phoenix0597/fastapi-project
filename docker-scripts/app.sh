#!/bin/bash
#alembic upgrade head && gunicorn -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker app.main:app
alembic upgrade head
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000