FROM python:3.8.3-buster
MAINTAINER Jonas.Winkler

COPY ./zhehe /zhehe

WORKDIR /zhehe

RUN pip install -r requirements/base.txt

COPY ./docker/zhehe/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN set -x \
    && apt-get update -y \
    && apt-get install -y poppler-utils \
    && apt-get install -y pandoc \
    && apt-get install -y texlive-full

ENTRYPOINT ["/entrypoint.sh"]