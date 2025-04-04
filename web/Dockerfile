FROM python:3.12-bookworm AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/web

RUN adduser \
    --system \
    --no-create-home \
    web-user

COPY . .

RUN sed -i 's/\r$//g' ./entrypoint.sh && \
    chmod +x ./entrypoint.sh

RUN mkdir -p /var/www/media /var/www/static && \
    chown -R web-user:users /var/www/media /var/www/static && \
    chmod -R 755 /var/www/media /var/www/static && \
    chmod -R g+s /var/www/media /var/www/static

RUN pip install --upgrade --root-user-action=ignore pip && \
    pip install -r requirements.txt

USER web-user

ENTRYPOINT ["./entrypoint.sh"]
