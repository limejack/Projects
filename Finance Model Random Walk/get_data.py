import constants
import requests

API_KEY = constants.API_KEY
url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey="+API_KEY

r = requests.get(url)
data = r.json()

with open("Data/IBM.json",'w') as outfile:
    outfile.write(str(data))
