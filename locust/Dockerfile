FROM locustio/locust
WORKDIR /locust-tests/
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt
COPY . .
