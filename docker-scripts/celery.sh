#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery -A app.tasks.celery_config:celery_app worker --loglevel=INFO --pool=solo --uid=nobody
elif [[ "${1}" == "flower" ]]; then
  celery -A app.tasks.celery_config:celery_app flower
fi
