First, start all the containers using your docker-compose file
Check for any containers that have a status of "exited" and restart these containers. In this case, the containers are named producer-1 and consumer-1.
Wait until the producer-1 container has a status of "exited".
Once the producer-1 container is in the "exited" state, you can access the data from the API at the following URL: http://localhost:5000/data
