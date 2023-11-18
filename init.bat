@echo off
echo Iniciando API
start /B uvicorn API.main:app --reload
start /B streamlit run API/app.py


