## Install Docker

Follow the instructions for your OS here: https://docs.docker.com/engine/install/

## Running the Application

Go into your project directory and open up your terminal. Type

```
docker-compose up
```

to build the project. The API will be available on port 5000 on your local machine.

To view model output, include this JSON object in your POST body:

```
{"spread": 10.5}
```
