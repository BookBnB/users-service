# pull official base image
FROM python:3.8.6-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=/app/project
ENV HOST=0.0.0.0

# copy project
COPY . /app

# install pyyaml
RUN apt-get update && \
    libyaml-dev && \
    pip uninstall pyyaml && \
    pip --no-cache-dir install pyyaml

# install dependencies
RUN pip install -r requirements.txt && \
    echo "FLASK_APP=project/" >> .env && \
    echo "FLASK_ENV=production" >> .env

EXPOSE $PORT

ENTRYPOINT /app/run.sh
