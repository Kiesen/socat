FROM python:3.7.0

ARG SRC_PATH=/usr/src/socat
ARG OUTPUT_PATH=/usr/src

WORKDIR $SRC_PATH

RUN mkdir -p $OUTPUT_PATH/data
RUN mkdir -p $OUTPUT_PATH/log

COPY .env $SRC_PATH
COPY src $SRC_PATH 
COPY requirements.txt $SRC_PATH

RUN pip install -r requirements.txt

CMD ["python", "-m", "unittest", "discover"] 