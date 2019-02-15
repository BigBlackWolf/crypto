# Crypto

[![Build Status](https://travis-ci.org/BigBlackWolf/crypto.svg?branch=master)](https://travis-ci.org/BigBlackWolf/crypto)

### Description
My pet project, here I am making crypto algorithms with web-interface.
In first version was released RSA encoding with Vue.js web interface


### Installation

##### Requirements:
* Python 3.6+
* Node.js 
* Redis
* Postgres 
* Linux


Change configurations in init.sql and config.py and then run:

Backend

```sh
$ source ./setup.sh
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
