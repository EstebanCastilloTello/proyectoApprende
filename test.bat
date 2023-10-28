@echo off

setlocal enabledelayedexpansion

set "init_flag=0"
set "stop_flag=0"
set "restart_flag=0"

REM Verificar si no se proporcionan argumentos y establecer init_flag en 1 por defecto
if "%~1"=="" set "init_flag=1"

:parse_args
if "%~1"=="" goto execute
if /I "%~1"=="-init" set "init_flag=1"
if /I "%~1"=="-stop" set "stop_flag=1"
if /I "%~1"=="-reset" set "restart_flag=1"
shift
goto parse_args

:execute
if !init_flag! equ 1 (
    echo Iniciando API
    start /B uvicorn API.main:app --reload
    start /B python -m http.server 8080 --directory web
)

if !stop_flag! equ 1 (
    echo Deteniendo API
    taskkill /f /im uvicorn.exe
    echo API detenida

    echo Deteniendo servidor web
    taskkill /f /im python.exe
    echo Servidor web detenido
)

if !restart_flag! equ 1 (
    echo Reiniciando procesos
    taskkill /f /im uvicorn.exe
    taskkill /f /im python.exe
    start /B uvicorn API.main:app --reload
    start /B python -m http.server 8080 --directory web
)

endlocal
