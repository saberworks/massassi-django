FROM python:3.9-slim-buster

WORKDIR /app/massassi-django

ARG APP_USER=massassi
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt update \
    && apt -y upgrade \
    && apt -y install libpq-dev build-essential python3-virtualenv virtualenv

ENV VIRTUAL_ENV=/app/massassi-django
RUN virtualenv -p python3 /app/massassi-django
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . ./massassi-django

USER ${APP_USER}:${APP_USER}

ENV DJANGO_SETTINGS_MODULE massassi.settings.dev

CMD ["gunicorn", "--chdir", "/app/massassi-django/massassi-django", "massassi.wsgi:application", "--bind", "0.0.0.0:8000"]
