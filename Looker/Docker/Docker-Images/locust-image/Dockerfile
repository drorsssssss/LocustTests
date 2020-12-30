# Start with a base Python 3.7 image that has chromedriver installed
FROM joyzoursky/python-chromedriver:3.7



ADD Looker/Docker/Docker-Images/locust-image/realbrowserlocusts /realbrowserlocusts

# Install the modified realbrowserlocusts package
RUN pip install realbrowserlocusts/.

# Expose the required Locust ports
EXPOSE 5557 5558 8089

# Install Message Queue implementation using redis
RUN pip install PyRSMQ

# Install Yml pkg for python
RUN pip install PyYAML

ADD LocustUtils/ /LocustUtils/

RUN pip install -e LocustUtils/

WORKDIR /usr/local/bin
ENTRYPOINT ["locust"]