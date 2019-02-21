# Crypto

[![Build Status](https://travis-ci.org/BigBlackWolf/crypto.svg?branch=master)](https://travis-ci.org/BigBlackWolf/crypto)

### Description
My pet project, here I am making crypto algorithms with web-interface.
In first version was released RSA encoding with Vue.js web interface


### Installation

Change configurations in config.py and then run:

##### Requirements:
* Docker
* Docker-compose

```bash
$ docker-compose up
```

To sync database:
```bash
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


### Tech stack

* Flask
* Node.js
* Vue.js
* Jinja2
* Bootstrap 3
* Postgres
* SQLAlchemy
* Celery
* RabbitMQ
* Docker

### Licence

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
