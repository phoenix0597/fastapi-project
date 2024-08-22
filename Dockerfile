FROM python:3.12.3-slim

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./docker-scripts/*.sh

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] # for DEV-ENV
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]