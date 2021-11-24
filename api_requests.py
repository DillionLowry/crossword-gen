import json
from json import encoder
import requests
import html

url = "https://www.xwordinfo.com/JSON/Data.aspx"

# For whatever reason the API will not return data on a get without the "Referer" header
my_headers = {
"Accept": "application/json",
"Accept-Encoding": "utf-8",
"Connection": "keep-alive",
"Referer": "https://www.xwordinfo.com/JSON/",
"Host": "www.xwordinfo.com"
}

date = "9/11/2008"

res = requests.get(url, headers=my_headers, params="date:"+date)
res.encoding='utf-8'
data=res.json(encoding='utf-8')

for x in range(len(data["answers"]["across"])):
    # the api returns escaped character and numbers before the answers so split on that and take second element
    print(html.unescape(data["answers"]["across"][x]), '\n', html.unescape(data["clues"]["across"][x]).split(". ")[1], sep="")