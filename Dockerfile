FROM python:3.10.18-slim-bullseye

WORKDIR /app/massassi-django

ARG APP_USER=massassi
RUN groupadd -r -g 1000 ${APP_USER} && \
    useradd --no-log-init -r -g ${APP_USER} -u 1000 ${APP_USER}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt update \
    && apt -y upgrade \
    && apt -y install libpq-dev build-essential python3-virtualenv \
                      virtualenv postgresql-client vim

RUN mkdir /massassi-user-data && chown massassi:massassi /massassi-user-data
RUN mkdir /jedibird-static && chown massassi:massassi /jedibird-static

ENV VIRTUAL_ENV=/app/massassi-django
RUN python3 -m venv /app/massassi-django/venv
SHELL ["/bin/bash", "-c"]
RUN ls -lh /app/massassi-django
RUN ls -lh /app/massassi-django/venv
RUN ls -lh /app/massassi-django/venv/bin
RUN source /app/massassi-django/venv/bin/activate

COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE massassi.settings.dev

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . ./massassi-django

RUN chown -R massassi:massassi /app/massassi-django/massassi-django

USER ${APP_USER}:${APP_USER}

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "--timeout", "300", "--chdir", "/app/massassi-django/massassi-django", "massassi.wsgi:application", "--bind", "0.0.0.0:8000"]
