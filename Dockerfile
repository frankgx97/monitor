FROM python:2.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN apk add --no-cache py-mysqldb \
&& pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD python /usr/src/app/run.py