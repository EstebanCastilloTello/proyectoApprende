#!/bin/bash
echo "Iniciando API"
uvicorn API.main:app --reload &
python -m http.server 8080 --directory web &