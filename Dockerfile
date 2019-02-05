FROM ubuntu:18.04

RUN mkdir /data/db
RUN mkdir /data/db/log

WORKDIR /usr/src/app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -y gnupg
RUN apt-get install -y build-essential
RUN apt-get install -y python3-pip

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list

RUN apt-get update

RUN apt-get install -y mongodb-org

RUN mongod --dbpath /data/db --fork --logpath /data/db/log

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade wheel
RUN python3 -m pip install --upgrade setuptools

RUN python3 -m pip install --upgrade pipenv

COPY . .

RUN pipenv sync

EXPOSE 80
EXPOSE 27017
EXPOSE 28017

RUN python3 install.py

CMD python3 run.py