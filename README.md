# weatherAuth
CRITICAL! Check your Api weather token plan, forecast could not work.

Weather server - flask_docker_2 writing in python. The new version weather_server but adding gRPC to touch Go auth server.
Auth server - auth_server, server on go with users hash-table.

Comands:

1. docker-compose up -d --build

Example: curl -H 'Own-Auth-UserName:user1' localhost:5000/current/city=Murmansk
