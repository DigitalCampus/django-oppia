FROM ghcr.io/astral-sh/uv:0.2.12 as uv
FROM python:3.8.19-slim-bullseye

RUN --mount=from=uv,source=/uv,target=./uv \
    ./uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /code

COPY . .

RUN apt-get update -y && \
    apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config && \
    pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=from=uv,source=/uv,target=./uv \
    ./uv pip install  -r requirements.txt

RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["sh", "/code/entrypoint.sh"]
