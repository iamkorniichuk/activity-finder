# syntax = docker/dockerfile:experimental
FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/web

RUN adduser \
    --system \
    --no-create-home \
    web-user

COPY . .

RUN sed -i 's/\r$//g' ./entrypoint.sh && \
    chmod +x ./entrypoint.sh

RUN mkdir -p /var/www/media /var/www/media/users /var/www/media/activities /var/www/static \
    && chown -R web-user:users /var/www/media/users /var/www/media/activities /var/www/media /var/www/static \
    && chmod -R 755 /var/www/media /var/www/media/users /var/www/media/activities /var/www/static \
    && chmod -R g+s /var/www/media /var/www/media/users /var/www/media/activities /var/www/static

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get install --no-install-recommends -y gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install --upgrade --root-user-action=ignore pip \
    && pip install -r requirements.txt

USER web-user

ENTRYPOINT ["./entrypoint.sh"]
