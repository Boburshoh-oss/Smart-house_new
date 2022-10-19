FROM python:3.10.4-alpine3.14

# Install dependencies required for psycopg2 python package
RUN apk update && apk add libpq
RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN chmod -R 777 /bin
RUN mv wait-for /bin/wait-for
RUN chmod -R 777 /bin/wait-for

RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

# Remove dependencies only required for psycopg2 build
RUN apk del .build-deps

EXPOSE 8000


