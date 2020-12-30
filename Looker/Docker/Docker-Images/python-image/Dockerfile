FROM python:3.8.6-alpine

# Install Message Queue implementation using redis
RUN pip install PyRSMQ

# Install Yml pkg for python
RUN pip install PyYAML

ADD LocustUtils/ /LocustUtils/

RUN pip install -e LocustUtils/

CMD ["python"]