#!/bin/sh

until cd /app/
do
    echo "Waiting for server volume..."
done

until alembic upgrade head
do
    echo "Waiting for db to be ready..."
    sleep 2
done

until python backend/initial_data.py
do
    echo "Waiting for initialization..."
    sleep2
done
