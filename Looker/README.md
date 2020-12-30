Looker Load Testing Tool
##
This tool runs a load test scenario, composed from 2 different tasks, upon a preconfigured Looker cluster.
Each task mimics a dashboard load, made by a virtual browser.

The scenario defined in the current script works as follows:
- A user perform a login to Looker instance using sellenium package.
  In order to have a unique login user, I'm using a message queue implementation with Redis.
  Each login task dequeue one user.
  
- After a succesfull login, 1 of 2 tasks performed in the following way:
  a. Dashboard load with normal data volume (Occur 80% of the times)
  b. Dashboard load with significant data volume (Occur 20% of the times)
    

Prerequisites
#############
1. Having docker & docker-compose installed
2. Build the base image for Looker load testing:  
   Run $ docker build -f /LocustTests/Looker/Docker/Docker-Images/locust-image/Dockerfile . -t dror_locust_looker
   * You should run this from /LocustTests folder.
   
3. Build the base image for Redis:   
   Run $ docker build -f Looker/Docker/Docker-Images/python-image/Dockerfile . -t py_redis
   * You should run this from /LocustTests folder.
   
4. Spin up the Redis instance:   
   - Go to Looker/Docker/Redis
   - Run $ docker-compose up -d
   
5. Insert accounts ids from csv file into Redis db:   
   a. Go to Looker/Local/IngestAccountsToRedis
   b. Change the accounts.csv file accordingly.
   c. Run $ docker run -it -v "$PWD":/redis/  py_redis python /redis/redisUtils.py
   
   You should see a message like this:
   "Number of added entries to queue: 100"
   
   
How to run this?
################

1. Go to Looker/Docker
2. Run docker-compose up

This command will spin up 2 containers:
a. Locust master container - This container will orchestrate the task submission on the different workers
b. Locust worker container - This container will act as a processing unit for running the Locust's test tasks defined in the script.
c. Go to <Host>:8089
   Now u can start running the Locust test
   
* It's possible to scale the number of workers by running:
  $ docker-compose up --scale worker=<number of workers> worker
