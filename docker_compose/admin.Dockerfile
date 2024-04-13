FROM python:3.11

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE 'config.settings'


COPY requirements requirements

RUN  pip install --upgrade pip \
     && pip install -r requirements

COPY ./docker_compose .

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver"]