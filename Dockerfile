FROM python:3.8
COPY src/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
