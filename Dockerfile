FROM openjdk:11

LABEL maintainer="nickrvieira at gmail.com"


WORKDIR /app
ENV JAR_CUSTOM_PATH /app/jars
ENV SLACK_CHANNELS="None"
ENV SLACK_BOT_TOKEN="Nope"
ENV PYSPARK_SUBMIT_ARGS="--jars ${JAR_CUSTOM_PATH}/postgresql-42.2.22.jar --driver-class-path ${JAR_CUSTOM_PATH}/postgresql-42.2.22.jar  pyspark-shell"

RUN apt update; \
    apt install -y python3 \
    python3-pip \
    wget; \
    ln -sL $(which python3) /usr/bin/python;

RUN mkdir -p ${JAR_CUSTOM_PATH} && wget -nc https://jdbc.postgresql.org/download/postgresql-42.2.22.jar -P ${JAR_CUSTOM_PATH}

COPY ./src .
COPY ./requirements.txt .


RUN python -m pip install -r requirements.txt 

ENTRYPOINT ["python","main.py"]
