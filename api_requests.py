import json
import requests

url = "https://www.xwordinfo.com/JSON/Data.aspx"

# For whatever reason the API will not return data on a get without the "Referer" header
my_headers = {
"Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Referer": "https://www.xwordinfo.com/JSON/",
"Host": "www.xwordinfo.com"
}

date = "9/11/2008"

res = requests.get(url, headers=my_headers, params="date:"+date)
data=res.json()
print(data["answers"]["across"])
