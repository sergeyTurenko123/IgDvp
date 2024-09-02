FROM python:latest 

WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src/ src/
COPY photoshare/ photoshare/
COPY tests/ tests/
COPY main.py main.py

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .