@echo off
cd /d "%~dp0"
py -3 -u server.py
if errorlevel 1 python -u server.py
pause
