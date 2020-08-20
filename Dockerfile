FROM alpine

FROM python:3.7

# Upgrade installed packages

COPY /mape /mape
COPY ./requirements.txt /mape

WORKDIR /mape
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install -y apache2-utils
RUN apt-get install -y apache2

ENTRYPOINT [ "python3" ,"-u"]

CMD [ "dockercompose_autoscale.py" ]
