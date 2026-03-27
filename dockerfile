FROM python:3.12.13-slim-trixie 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app
ENV WMS_HOME=/app/wms

RUN mkdir -p $APP_HOME
RUN mkdir -p $WMS_HOME

COPY ./requirements.txt $APP_HOME
COPY ./scripts/entrypoint.sh $APP_HOME
COPY ./src $WMS_HOME

WORKDIR $APP_HOME

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x $APP_HOME/entrypoint.sh

WORKDIR $WMS_HOME

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
