FROM python:3.9-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app

EXPOSE 8000

CMD [ "python","/app/driver.py"]

