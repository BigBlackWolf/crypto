# Crypto

[![Build Status](https://travis-ci.org/BigBlackWolf/crypto.svg?branch=master)](https://travis-ci.org/BigBlackWolf/crypto)

### Description
My pet project, here I am making crypto algorithms with web-interface.
In first version was released RSA encoding with Vue.js web interface


### Installation

#### Easy way: 

##### Requirements:
* Docker
* Docker-compose

```bash
$ docker-compose up
```

To init database:
```bash
$ docker exec flask_crypto_db_1 /bin/sh -c "psql -U crypto_user -f docker-entrypoint-initdb.d/init.sql"
$ docker exec flask_crypto_server_1 /bin/sh -c "flask db migrate && flask db upgrade"
# Optional to init user
$ docker exec flask_crypto_db_1 /bin/sh -c "psql -U crypto_user aiohttp_crypto -c "INSERT INTO users(cookie) VALUES ('test');""
```

#### Long way:

##### Requirements:
* Python 3.6+
* Node.js 
* Redis
* Postgres 
* Linux


Change configurations in init.sql and config.py and then run:

Backend

* Python requirements:
```sh
$ vitrualenv venv
$ source venv/bin/activte
$ pip install -r requirements.txt
```

* Postgres requirements (don't forget to change init.sql):
```sh
$ psql -U postgres postgres -f ./init.sql
$ python run.py db init
$ python run.py db migrate
$ python run.py db upgrade
```

* Task runner requirements:
```sh
$ redis-server
$ celery -A app.tasks worker --loglevel=info
$ python run.py runserver
```

Frontend 

```sh
$ cd frontend 
$ npm install
$ npm run dev
```


### Tech stack

* Flask
* Node.js
* Vue.js
* Jinja2
* Bootstrap 3
* Postgres
* SQLAlchemy
* Celery
* Redis

### Licence

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
