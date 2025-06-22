@echo off
setlocal

echo.
echo ---Start Celery worker---
start "" /B cmd /c "celery -A SmartStudy.celery_config worker -l info -P gevent"

REM Wait for 3 seconds
timeout /t 3 /nobreak > nul

echo.
echo ---Start Celery beat---
start "" /B cmd /c "celery -A SmartStudy.celery_config beat --loglevel=info"

endlocal
