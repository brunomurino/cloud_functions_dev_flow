
FROM python:3.8

ARG GCP_CREDENTIALS_FILENAME
ARG FUNCTIONS_JOB_NAME

ENV GOOGLE_APPLICATION_CREDENTIALS=/root/config/$GCP_CREDENTIALS_FILENAME.json \
    JOB_NAME=$FUNCTIONS_JOB_NAME

COPY ./ /root/function/

RUN pip install --upgrade pip && \
    pip install functions-framework && \
    pip install -r /root/function/requirements.txt

WORKDIR /root/function/