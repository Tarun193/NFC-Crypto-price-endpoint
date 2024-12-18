from os import getenv
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import flask

import threading
import asyncio

app = flask.Flask(__name__)
# Loading environment variables
load_dotenv()

# coin list
coins = ["xrp", "render"]

# API url to call
url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"

# Parameter with which we gonna call the API
parameters = {"slug": ",".join(coins), "convert": "CAD"}

# Header for setting up the datatype and authentication
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": getenv("API_KEY"),
}


def Get_Data():
    # Starting a session and calling the API
    session = Session()
    session.headers.update(headers)
    price = []

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        data = data["data"]

        for key in data:
            price.append(data[str(key)]["quote"]["CAD"]["price"])
        print(price)
        return list(zip(coins, price))

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)





def FormatData(data):
    return "\n".join(f"{x}: {int(y*100)/100} CAD" for x, y in data)



@app.route("/")
def SendData():
    response_data = {
        "status": "success",
        "message": "This is a JSON response from Flask",
        "data": FormatData(Get_Data()),
    }
    print(response_data)
    return flask.jsonify(response_data)


app.run()
