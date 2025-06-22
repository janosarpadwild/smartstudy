@echo off
setlocal

echo ---Start PostgreSQL database---
start "" /B cmd /c "pg_ctl -l logfile start"

REM Wait for 3 seconds
timeout /t 3 /nobreak > nul

echo.
echo ---Test database connection---
pg_isready > pg_isready_output.txt
timeout /t 3 /nobreak > nul
type pg_isready_output.txt

echo.
echo ---Start Redis server---
start "" /B wsl -e sh -c "echo YOUR_WSL_PASSWORD | sudo -S service redis-server start"

REM Wait for 3 seconds
timeout /t 3 /nobreak > nul

echo.
echo ---Test server connection---
wsl -e sh -c "redis-cli ping" > redis_ping_output.txt
timeout /t 3 /nobreak > nul
type redis_ping_output.txt

REM Wait for 3 seconds
timeout /t 3 /nobreak > nul

endlocal
