FROM python:3.9-slim

RUN pip install poetry

WORKDIR /app

RUN pip install gunicorn==19.9.0
RUN poetry config virtualenvs.create false
ADD pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-interaction --no-ansi


COPY . .

ENTRYPOINT [ "gunicorn", "ide_proxy.wsgi", "-b", "0.0.0.0:9000" ]