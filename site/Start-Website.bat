@echo off
cd /d "%~dp0"
echo Starting Indore Nursery preview at http://localhost:8080 ...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve.ps1"
