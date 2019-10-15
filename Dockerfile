# Dockerfile for building larpix-db django application
FROM python:3

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    fonts-liberation

ARG PROJECT_DIR=/app

RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

COPY requirements.txt $PROJECT_DIR
RUN pip install -r requirements.txt
# COPY * $PROJECT_DIR/

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0:8000"]
