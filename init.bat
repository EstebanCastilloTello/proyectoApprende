@echo off
echo Iniciando API
start /B uvicorn API.main:app --reload
start /B python -m http.server 8080 --directory web
