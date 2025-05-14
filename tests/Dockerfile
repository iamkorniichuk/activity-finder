FROM python:3.12-bookworm AS build

WORKDIR /var/www/tests

COPY . .

RUN pip install --upgrade --root-user-action=ignore pip && \
    pip install -r requirements.txt

CMD ["pytest", "-n", "auto"]
