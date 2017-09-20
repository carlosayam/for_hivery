FROM python:3

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y build-essential

## RUN apt-get install

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7777
CMD [ "uwsgi", "wsgi.ini" ]
