"""
A simple api built with FastAPI
"""

from fastapi import FastAPI, HTTPException
from tinydb import TinyDB, Query
from statistics import median

app = FastAPI()

mock_db = TinyDB("mock_data.json")
Odds = Query()


@app.get("/")
def read_root():
    """The root / home page"""
    return {"Hello": "FastAPI"}


@app.get("/odds/{game_id}/{market_type}/last")
async def most_recent_doc(game_id, market_type):
    """Return the most recent game data
    ATTENTION: For getting the most recent game data
    we implicitly depend on the db engine. Any change
    to it, will break the API contract, in an non obvious way
    """
    ## get the data - most recent document
    try:
        query_result = mock_db.search(
            (Odds.gameId == f"{game_id}") & (Odds.marketType == f"{market_type}")
        )[
            -1
        ]  ## last document is most recent
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="There is an Internal Server Error",
            headers={
                "X-Error": f"There is something wrong with the database connection. This is the error returned: {e}"
            },
        )

    ## return results
    if query_result:
        return query_result
    else:  ## empty response
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={
                "X-Error": "Empty response from the database. Check gameId and marketType"
            },
        )


@app.get("/odds/{game_id}/{market_type}/average")
async def average_odds(game_id, market_type):
    """Return the average odds for an event and market"""
    ## get the data - collection of documents
    try:
        query_result = mock_db.search(
            (Odds.gameId == f"{game_id}") & (Odds.marketType == f"{market_type}")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="There is an Internal Server Error",
            headers={
                "X-Error": "There is something wrong with the database connection"
            },
        )

    ## return results
    if query_result:
        ## Compute requested fields
        response_template = query_result[0]

        odds1, oddsx, odds2 = [], [], []
        time_snapshots = []
        bookies = []

        for doc in query_result:
            odds1.append(doc["odds1"])
            oddsx.append(doc["oddsX"])
            odds2.append(doc["odds2"])
            time_snapshots.append(doc["timeReceived"])
            bookies.append(doc["bookmakerName"])

        ## use the median - simple way to eschew outlies
        av_odds1 = median(odds1)
        av_oddsx = median(oddsx)
        av_odds2 = median(odds2)

        first_snapshot = time_snapshots[0]
        last_snapshot = time_snapshots[-1]
        number_of_bookies = len(set(bookies))

        ## Build response
        response = {
            "awayTeamId": response_template["awayTeamId"],
            "awayTeamName": response_template["awayTeamName"],
            "competitionId": response_template["competitionId"],
            "gameId": response_template["gameId"],
            "homeTeamId": response_template["homeTeamId"],
            "homeTeamName": response_template["homeTeamName"],
            "marketType": response_template["marketType"],
            "averageOdds1": av_odds1,
            "averageOdds2": av_odds2,
            "averageOddsX": av_oddsx,
            "seasonId": response_template["seasonId"],
            "firstTimeSnapshot": first_snapshot,
            "lastTimeSnapshot": last_snapshot,
            "NumberOfBookmakers": number_of_bookies
        }
        return response

    else:  ## case of empty response
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={
                "X-Error": "Empty response from the database. Check gameId and marketType"
            },
        )
