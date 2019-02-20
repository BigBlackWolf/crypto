FROM python:3.7.2-alpine3.9

WORKDIR /work

COPY . .

RUN \
 apk update && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN ["pip", "install", "-r", "requirements.txt"]

EXPOSE 5000

CMD python run.py runserver --host 0.0.0.0