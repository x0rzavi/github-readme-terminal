# reference: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
FROM python:alpine as builder
RUN pip install poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
WORKDIR /app
RUN touch README.md
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-directory

FROM python:alpine as runtime
RUN apk add --no-cache ffmpeg
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY gifos ./src/gifos
COPY fonts ./src/fonts
COPY config ./src/config
COPY main.py ./src
ENTRYPOINT ["python", "./src/main.py"]
