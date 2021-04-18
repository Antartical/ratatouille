#!/bin/bash

set -e

MAX_POSTGRES_RETRIES=60
MAX_ELASTICSEARCH_RETRIES=60

check_service(){
    counter=1
    while ! nc -w 1 "$1" "$2" > /dev/null 2>&1; do
        sleep 1
        counter=`expr ${counter} + 1`
        if [[ ${counter} -gt ${3} ]]; then
            >&2 echo "SERVICE $1:$2 NOT AVAILABLE"
            exit 1
        fi;
    done
}

migrate(){
    if ! [[ "$ENVIRONMENT" == "production" ]]; then
        aerich upgrade;
        python manage.py elastic build;
    fi
}

health_check(){
    check_service "$POSTGRES_HOST" "$POSTGRES_PORT" "$MAX_POSTGRES_RETRIES"
    check_service "$ELASTICSEARCH_HOST" "$ELASTICSEARCH_PORT" "$MAX_ELASTICSEARCH_RETRIES"
}


health_check
migrate
if [[ "$1" == "serve" ]]; then
    exec uvicorn ratatouille.asgi:app \
    --host 0.0.0.0 \
    --port ${RATATOUILLE_PORT} \
    --workers ${RATATOUILLE_WORKERS}
elif [[ "$1" == "serve:watch" ]]; then
    # health_check
    exec uvicorn ratatouille.asgi:app \
    --host 0.0.0.0 \
    --port ${RATATOUILLE_PORT} \
    --workers ${RATATOUILLE_WORKERS} \
    --reload
fi


# system_setup
exec $@
