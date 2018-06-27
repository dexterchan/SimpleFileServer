#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM python:3.7.0b5-slim-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /usr/src/app/uploads

COPY FILEIO ./FILEIO
COPY templates ./templates
COPY SimpleFileServer.py ./

#CMD [ "/bin/bash" ]
CMD [ "python", "./SimpleFileServer.py" ]