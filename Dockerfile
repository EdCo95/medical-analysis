FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y wkhtmltopdf \
    && apt-get clean

WORKDIR /app

COPY . /app

RUN pip install -U pip setuptools wheel
RUN pip install .

ENTRYPOINT ["python", "run.py"]
