FROM python:3.6-alpine AS base

RUN pip install --no-cache-dir newrelic

ENTRYPOINT ["newrelic-admin", "run-program"]

FROM base AS final

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN mkdir logs

ENV NEW_RELIC_LOG=stdout

CMD [ "python3", "synology-photos.py"]
