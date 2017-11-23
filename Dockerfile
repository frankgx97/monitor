FROM alpine:3.6

WORKDIR /usr/src/app

COPY . .

RUN set -ex  \
&& echo "http://mirrors.ustc.edu.cn/alpine/v3.6/main/" > /etc/apk/repositories \
&& echo "http://mirrors.ustc.edu.cn/alpine/v3.6/community/" >> /etc/apk/repositories \
&& apk add --no-cache --virtual .build-deps mariadb-dev mariadb-client mariadb-libs gcc python-dev py-pip musl-dev linux-headers\
&& pip install --no-cache-dir -r requirements.txt \
&& apk del .build-deps \
&& apk add --no-cache python mariadb-libs mariadb-client

EXPOSE 5000

CMD python /usr/src/app/run.py