FROM python:3.10-slim-buster

ARG KAFKA_BROKER
ARG KAFKA_TOPIC
ARG KAFKA_GROUP_ID
ARG MYSQL_HOST
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_DATABASE
ARG REDIS_HOST
ARG REDIS_PORT
ARG API_HOST

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN sed -i "s|kafka_broker_value|$KAFKA_BROKER|g" src/utils/config.py
RUN sed -i "s|kafka_topic_value|$KAFKA_TOPIC|g" src/utils/config.py
RUN sed -i "s|kafka_group_id_value|$KAFKA_GROUP_ID|g" src/utils/config.py
RUN sed -i "s|mysql_host_value|$MYSQL_HOST|g" src/utils/config.py
RUN sed -i "s|mysql_user_value|$MYSQL_USER|g" src/utils/config.py
RUN sed -i "s|mysql_password_value|$MYSQL_PASSWORD|g" src/utils/config.py
RUN sed -i "s|mysql_database_value|$MYSQL_DATABASE|g" src/utils/config.py
RUN sed -i "s|redis_host_value|$REDIS_HOST|g" src/utils/config.py
RUN sed -i "s|redis_port_value|$REDIS_PORT|g" src/utils/config.py
RUN sed -i "s|api_host_value|$API_HOST|g" src/utils/config.py


CMD [ "python", "-u" , "src/__main__.py"]