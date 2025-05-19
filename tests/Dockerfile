# syntax = docker/dockerfile:experimental
FROM python:3.12-bookworm

WORKDIR /var/www/tests

COPY . .

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install --upgrade --root-user-action=ignore pip \
    && pip install -r requirements.txt

CMD ["pytest", "-n", "auto"]
