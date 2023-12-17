## A simple API

The purpose of this mini project is to built a simple API that serves data from a database. This is how it is structured:

There is document database that sits in the background, loaded with data. In our case, we will built a simple mock for MongoDB, using TinyDB a flat-file or in-memory replacement for MongoDB. We will load it with some documents, enough to demonstrate how the API works.

#### The data

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

#### The objective

There is an RESTful API built with FastAPI, that has two GET endpoints:
- one that returns the most recent odds for the specified game and market, together with metadata, and
- another that returns the average odds for the specified game and market, together with metadata. 

Metadata include time the record was received, team names, gameDate, etc.

This simple app runs inside a docker container, and the provided Dockerfile and docker-compose.yml, build the whole thing.

#### How to run the solution:

We have included a docker-compose.yml file with the instructions on running the solution. Navigate to the repository, and in a terminal enter:

> docker-compose up 

Docker will build the image, and start the container.
 
Now we are ready to access our app. Go to
> http://localhost/docs

and verify that the app is up an running.

In the main page, you will be greeted with a simple "Hello World" message.
> http://localhost/

In the two main routes we have implemented the requirements.

For example, for gameId = 54321 and the '1x2' market, for the most recent document in the database go to:

> http://localhost/odds/54321/1x2/last

while for the average odds go:

> http://localhost/odds/54321/1x2/average

#### The architecture
A simple one file FastAPI, found in the folder `app` does all the work.

In the app folder you will also find a json file with data mocking an actual database.

In the main file, we read the data from the 'database', prepare, and serve the responses.

In the root folder, there are the docker files for running the solution, and this brief README.
