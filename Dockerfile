# Dockerfile

FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install mysql-connector-python

CMD ["python", "server.py"]



