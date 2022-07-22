FROM python:3.8-slim

LABEL author='rm@ipadla.org' version=2

RUN mkdir /app
COPY ./ /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
WORKDIR /app
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
