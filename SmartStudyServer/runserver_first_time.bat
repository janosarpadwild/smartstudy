@echo off
setlocal

python manage.py reset_db --noinput

echo.
echo ---Make migrations---
python manage.py makemigrations

echo.
echo ---Apply migrations---
python manage.py migrate

echo.
echo ---Populate database---
python manage.py populate_database

echo.
echo ---Start Django Server---
python manage.py runserver_plus --cert-file certificate/localhost.crt

endlocal
