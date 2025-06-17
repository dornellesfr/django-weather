FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Mostra os logs na tela
ENV PYTHONUNBUFFERED=1 
# Não escreve arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml ./

RUN uv venv

RUN uv sync

COPY . .

RUN mkdir -p /app/staticfiles

RUN uv run python manage.py collectstatic --noinput --clear

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]