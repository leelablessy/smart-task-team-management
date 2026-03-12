@echo off
cd /d "%~dp0backend"
myvenv\Scripts\python seed_admin.py
pause
