#syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY .env .
COPY /setup.py .
COPY /server .
CMD ["python", "app.py"]
