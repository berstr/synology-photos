

## Env Variables

    export NEW_RELIC_LICENSE_KEY=XXXX
    export NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=XXX
    export NEW_RELIC_APP_NAME=XXXX

    export SYNOLOGY_FILESTATION_SERVICE = None  # <hostname>:<port>  ... not used yet
    export SYNOLOGY_HOST=XXXX  # <hostname>:<port>
    export SYNOLOGY_USERNAME = None
    export SYNOLOGY_PASSWORD = None

----------------

## CLI

Manual start from command line:

newrelic-admin run-program python3 synology-photos.py

---------------------

## Docker

X.Y is the image tag

    docker build -t berndstransky/synology-photos:X.Y .

    docker push berndstransky/synology-photos:X.Y

On VM:

    docker run -d --name synology-photo -e NEW_RELIC_LICENSE_KEY -e NEW_RELIC_DISTRIBUTED_TRACING_ENABLED -e NEW_RELIC_APP_NAME -e SYNOLOGY_USERNAME -e SYNOLOGY_PASSWORD -e SYNOLOGY_HOST -v /var/log/container:/logs -p37083:37083 berndstransky/synology-photos:X.Y

On Macbook:

    docker run -d --name synology-photo -e NEW_RELIC_LICENSE_KEY -e NEW_RELIC_DISTRIBUTED_TRACING_ENABLED -e NEW_RELIC_APP_NAME -e SYNOLOGY_USERNAME -e SYNOLOGY_PASSWORD -e SYNOLOGY_HOST -v $(pwd)/logs:/logs -p37083:37083 berndstransky/synology-photos:X.Y
