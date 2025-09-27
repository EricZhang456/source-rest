# syntax=docker/dockerfile:1.4
FROM python:3.13.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["fastapi", "run", "--app", "app"]
CMD ["--port", "8000"]

EXPOSE 8000
