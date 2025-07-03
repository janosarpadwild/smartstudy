# smartstudy
The SmartStudy app is a Django-based educational platform that facilitates student management, class organization, and teacher-student interactions through a RESTful API.

# 🐍 Python + Django + PostgreSQL + Redis Install Guide (Windows)

## 1. Install Python 3.12.2

- Download from: [https://www.python.org/downloads/release/python-3122/](https://www.python.org/downloads/release/python-3122/)
- Recommended: **Windows installer (64-bit)**
- During installation:
  - ✅ Check: **Add python.exe to PATH**
  - 🚀 Click: **Install Now**
  - ✅ Allow permission prompts
  - ✅ Accept option to **disable path length limit**

---

## 2. Install Required Python Libraries

Open `cmd.exe` and run:

```bash
pip install django
pip install django-redis
pip install djangorestframework
pip install django-extensions
pip install celery
pip install gevent
pip install psycopg
pip install werkzeug
pip install python-docx
pip install pyqt6
```

---

## 3. Install Redis on Windows Subsystem for Linux (WSL)

### 3.1 Install WSL

```bash
wsl --install
```

- Reboot after installation
- Choose a Linux username/password when prompted

### 3.2 Install Redis on WSL

```bash
wsl
sudo apt-get update
sudo apt-get install redis
sudo service redis-server restart
redis-cli
ping  # Should return PONG
exit
```

---

## 4. Install PostgreSQL 16

- Download from: [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- Choose: **Windows x86-64**

### Installation steps

- Keep default installation directories
- Set and remember the **password**
- Optionally add to `PATH`:
  ```
  C:\Program Files\PostgreSQL\16\bin
  ```
- Optionally set `PGDATA`:
  ```
  Variable: PGDATA
  Value:    C:\Program Files\PostgreSQL\16\data
  ```

### Starting PostgreSQL

```bash
pg_ctl -l logfile start
```

To stop:

```bash
pg_ctl stop
```

To check readiness:

```bash
pg_isready
```

### Create Database

Open:

```bash
C:\Program Files\PostgreSQL\16\pgAdmin 4\runtime\pgAdmin.exe
```

- Navigate: `Servers > Databases > Create > Database`
- Name: `smart_study`

---

## 5. Run Services and Django Server

### Start Redis

```bash
wsl
sudo service redis-server start
```

Check:

```bash
redis-cli ping
```

### Start Celery (in project folder)

```bash
celery -A SmartStudy.celery_config worker --loglevel=info
celery -A SmartStudy.celery_config beat --loglevel=info
```

### Setup Django (first run only)

```bash
cd SmartStudyServer
python manage.py reset_db --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py populate_database
```

### Run Django server

```bash
python manage.py runserver_plus --cert-file certificate/localhost.crt
```

### Create admin user

```bash
python manage.py createsuperuser
```

---

> ✅ Your Django server should now be fully functional with PostgreSQL, Redis, and Celery integration on Windows.
