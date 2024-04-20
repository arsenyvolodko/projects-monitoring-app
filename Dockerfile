##CMD ["poetry", "run", "gunicorn", "django_api_files.wsgi:application", "--bind", ":8000"]
#CMD ["gunicorn", "-c", "conf/gunicorn_config.py", "junior_team.wsgi"]

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.7.1

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["poetry", "run", "gunicorn", "-c", "conf/gunicorn_config.py", "junior_team.wsgi"]
