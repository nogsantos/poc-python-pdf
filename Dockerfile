FROM python:3.7

RUN mkdir /poc_python_pdf
WORKDIR /poc_python_pdf
COPY ./requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev &&  \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/archive/*.deb

RUN pip3 install -r requirements.txt

COPY . .

RUN cp contrib/env.sample .env

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

RUN rm -rf contrib/ .env