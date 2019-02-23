FROM python:3.6-alpine
COPY ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add gcc g++ \
    && apk add linux-headers\
    && apk add bash git gifsicle
RUN pip3 install cython
RUN pip3 install -r requirements.txt
COPY . /code
CMD ["gunicorn", "--log-level=debug", "--workers=2", "--name=mock_mosaic_maker", "--bind=0.0.0.0:5080", "--timeout=160", "wsgi:app"]
