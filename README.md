## A simple API

The purpose of this mini project is to built a simple API that serves data from a database. This is how it is structured:

There is document database that sits in the background, loaded with data. In our case, we will built a simple mock for MongoDB, using TinyDB a flat-file or in-memory replacement for MongoDB. We will load it with some documents, enough to demonstrate how the API works.

The data domain is from the betting industry, with odds/prices for sports events. This is an example for a document:
```
{
    "_id": "...",
    "awayTeamId": "...",
    "bookmakerId": 18,
    "bookmakerName": "PinnacleSports",
    "competitionId": "...",,
    "gameId": "...",
    "homeTeamId": "...",
    "marketType": "1x2",
    "odds1": 1.73,
    "odds2": 5.24,
    "oddsX": 3.51,
    "seasonId": 2021,
    "source": "oddsportal",
    "timeReceived": {
        "$date": {
            "$numberLong": "1629698330000"
            }
        }
}
```

There is an RESTful API built with FastAPI, that has two GET endpoints:
- one that returns the most recent odds for the specified game and market, together with metadata, and
- another that returns the average odds for the specified game and market, together with metadata. 

Metadata include time the record was received, team names, gameDate, etc.

This simple app runs inside a docker container, and the provided Dockerfile builds the whole thing.

How to run the solution:

First we have to build the Docker image

Go to the project directory (in where your Dockerfile is, containing your app directory).
   
Build your FastAPI image:

> $ docker build -t myimage .

Then we can start the Docker Container service

To do so, run a container based on the image we just created:

> $ docker run -d --name mycontainer -p 80:80 myimage

With the -d flag the container will run in the background and serve the API calls.

To stop that container, and the service, we should run:
> $ docker container stop mycontainer

Containers are disposable, so we can delete with the prune command that will delete all stopped containers - be careful not to delete something you actually want to restart!
> $ docker container prune
 
Now we are ready to access our app. Go to
> http://localhost/docs

and verify that the app is up an running.

For now, you will be greeted with a simple "Hello World" message if you go to home directory
> http://localhost/


