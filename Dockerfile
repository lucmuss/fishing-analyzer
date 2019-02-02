FROM ubuntu:18.04
# Ubuntu Installation
RUN apt-get update
# Paket Manager Update
RUN apt-get install build-essential
RUN apt-get install python3-pip
RUN apt-get install mongodb-org
# Installation von MongoDB
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade wheel
RUN python3 -m pip install --upgrade setuptools
# Installation der Python Paket Manager
# RUN python3 -m pip install --upgrade pipenv
# Installation von Virtual Env
WORKDIR /usr/src/app
# Arbeitsverzeichnis wechseln
COPY requirements.txt ./
# Requirements kopieren
# RUN pipenv install -r requirements.txt
RUN pip install -r requirements.txt
# Software Abhängigkeiten installieren
COPY . .
# Verzeichnis kopieren
EXPOSE 80
# Port freischalten
RUN python3 install.py
CMD [ "python3", "./run.py" ]
# App und Server starten