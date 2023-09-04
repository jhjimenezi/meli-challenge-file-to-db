FROM python:3.10-slim-buster

ARG INPUT_FILE_LOCATION
ARG KAFKA_BROKER
ARG KAFKA_TOPIC
ARG CHUNK_SIZE

RUN echo "Kafka broker: $KAFKA_BROKER"

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN sed -i "s|INPUT_FILE_LOCATION_VALUE|$INPUT_FILE_LOCATION|g" conf/app.conf
RUN sed -i "s|KAFKA_BROKER_VALUE|$KAFKA_BROKER|g" conf/app.conf
RUN sed -i "s|KAFKA_TOPIC_VALUE|$KAFKA_TOPIC|g" conf/app.conf
RUN sed -i "s|CHUNK_SIZE_VALUE|$CHUNK_SIZE|g" conf/app.conf

CMD [ "flask", "--app" , "src/__main__.py", "run", "-h", "0.0.0.0", "-p", "5001"]