FROM python:3.6-alpine

WORKDIR /usr/src/app

#Copy requirements
COPY requirements.txt /tmp
COPY . ./
#Install requirements
RUN pip3 install -r /tmp/requirements.txt
