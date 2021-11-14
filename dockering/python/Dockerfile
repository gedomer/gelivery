FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN ls requirements
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r requirements/base.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app
ENV PATH="/py/bin:$PATH"
EXPOSE 8000
