FROM python:3.10-slim-buster

LABEL maintainer="Sohype Khaled"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && \
    apt-get install -y postgresql-client gettext && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
COPY . /app

WORKDIR /app

RUN python3 -m venv --system-site-packages /py && \
    /py/bin/pip3 install --upgrade pip && \
    /py/bin/pip3 install -r /requirements.txt

ENV PATH="/py/bin:$PATH"

ARG UNAME=app
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID $UNAME && \
    useradd -u $UID -g $GID --no-create-home $UNAME  && \
    mkdir -p /app/static && \
    mkdir -p /app/media && \
    mkdir -p /app/staticfiles && \
    chown -R app:app /app/static && \
    chmod -R 775 /app/static && \
    chown -R app:app /app/staticfiles && \
    chmod -R 775 /app/staticfiles && \
    chown -R app:app /app/media && \
    chmod -R 775 /app/media && \
    chown -R app:app /app && \
    find . -type d -exec chmod 755 {} \; && \
    find . -type f -exec chmod 644 {} \;

USER app

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 2 app.wsgi:application --log-level debug"]
