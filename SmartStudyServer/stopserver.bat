@echo off
setlocal

echo ---Stop Celery beat---
echo ---Stop Celery worker---
taskkill /F /IM "celery.exe" /T

echo ---Stop Redis server---
start "" /B wsl -e sh -c "echo YOUR_WSL_PASSWORD | sudo -S service redis-server stop"

REM Wait for 3 seconds to ensure the service stops
timeout /t 3 /nobreak > nul

echo ---Stop PostgreSQL database---
pg_ctl stop

REM Wait for 3 seconds to ensure the service stops
timeout /t 3 /nobreak > nul

endlocal
