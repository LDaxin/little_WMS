FROM python:3.12.13-slim-trixie 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/app

RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

COPY ./requirements.txt .
COPY ./entrypoint.sh .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x $APP_HOME/entrypoint.sh

WORKDIR $APP_HOME/wms
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
