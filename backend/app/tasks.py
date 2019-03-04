from celery import Celery
from rsa.rsa import RSA

worker = Celery(__name__, broker='amqp://ampq:5672', backend='amqp://ampq:5672')


@worker.task(bind=True)
def generate(self, length):
    rsa = RSA(length)
    keys = dict(modulus=hex(rsa.modulus)[2:],
                exponent=hex(rsa.exponent)[2:],
                secret=hex(rsa.secret)[2:])
    return keys


@worker.task(bind=True)
def transform(self, **kwargs):
    result = RSA._hex_to_int(**kwargs)
    return result


@worker.task(bind=True)
def encrypt(self, **kwargs):
    encrypted = RSA.encrypt(**kwargs)
    return {'encrypted': encrypted}


@worker.task(bind=True)
def verify(self, **kwargs):
    verified = RSA.verify(**kwargs)
    return {'verified': verified}
