from celery import Celery
from app.rsa import RSA

worker = Celery(__name__, broker='redis://localhost:6379', backend='redis://localhost:6379')


@worker.task(bind=True)
def celery_generate(self, length):
    rsa = RSA(length)

    keys = dict(module=hex(rsa.modulus)[2:],
                public_exponent=hex(rsa.exponent)[2:],
                secret=hex(rsa.secret)[2:])
    return keys
