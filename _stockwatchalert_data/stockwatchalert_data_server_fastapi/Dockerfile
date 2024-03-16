# python smallest image
FROM python:3.9-bullseye

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip

COPY .env ./
COPY ./app ./app
COPY ./_project ./_project

ARG WORKERS=8
ARG PRODUCTION=True
ENV WORKERS=${WORKERS}
ENV PRODUCTION=${PRODUCTION}

CMD exec uvicorn app.main:app --host=${HOST} --port=${PORT} --workers=${WORKERS}
