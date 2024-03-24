# python smallest image
FROM python:3.10.13-slim-bullseye

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip

COPY .env ./
COPY ./app ./app
COPY ./_project/data/fmp ./_project/data/fmp
COPY ./_project/data/results ./_project/data/results
COPY ./_project/data/symbols ./_project/data/symbols
COPY ./_project/log_config ./_project/log_config
COPY ./_project/signals ./_project/signals

ARG WORKERS=8
ARG PRODUCTION=True
ENV WORKERS=${WORKERS}
ENV PRODUCTION=${PRODUCTION}

CMD exec uvicorn app.main:app --host=${HOST} --port=${PORT} --workers=${WORKERS}
