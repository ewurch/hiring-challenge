FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry export -f requirements.txt --output requirements.txt

RUN pip install -r /app/requirements.txt

COPY /src /app

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]