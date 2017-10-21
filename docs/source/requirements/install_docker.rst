Installing via Docker
=====================
In order to install the Hutts Verification system by making use of Docker,
please make sure that `Docker is installed on your system <https://docs.docker.com/engine/installation/>`_
before proceeding with the installation.

Run the following commands in order to get started with Docker::

    docker pull andreasnel/jhutts:latest
    docker run -d --rm -p <your preferred port>:5000 andreasnel/jhutts

That's it! You can now make requests to the server running in the docker container exactly like in our section **Using the Server**.
