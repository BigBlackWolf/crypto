# Crypto

## Build with Docker

Requires [Docker](https://docs.docker.com/install/) 
and [docker-compose](https://docs.docker.com/compose/install/).

Assuming you are in project root directory:

```bash
docker-compose up
```

Frontend should be serving at `127.0.0.1:8080`

Server should be at `127.0.0.1:5000`

## Build without Docker

Requires [python 3.6](https://www.python.org/downloads/) or higher,
[node.js](https://nodejs.org/en/download/) and [npm](https://docs.npmjs.com/cli/install),
[postgresql](https://www.postgresql.org/download/)

First, setup database

```bash
psql -f init.sql
```

Then, run server app

```bash
cd server/
# OPTIONAL BUT HIGHLY RECOMMENDED
#
# virtualenv venv
# source venv/bin/activate
pip install -r requirements.txt
python run
python run.py runserver
```

After that, in another terminal/tab/pane/whatever run frontend app

```bash
cd frontend/
npm install
npm run dev
```

Frontend should be serving at `127.0.0.1:8080`

Server should be at `127.0.0.1:5000`

## Migrations

Migrations are stored at `server/migrations`. To apply your changes, run

```bash
python run.py db migrate
```

And then reup your docker-compose or (in case of native setup) run

```bash
python run.py db upgrade
```
