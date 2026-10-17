#!/bin/sh

set -e

if [ ! -f /data/pokemon.db ]; then
    echo "Inicializando la base de datos"
    python seed.py
fi

exec uvicorn main:app --host 0.0.0.0 --port 8000