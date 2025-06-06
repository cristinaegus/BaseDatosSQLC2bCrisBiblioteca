@echo off
REM Script para arrancar FastAPI con main_api2.py en el puerto 8020
cd /d %~dp0
uvicorn biblioteca.main_api2:app --reload --port 8020
pause
