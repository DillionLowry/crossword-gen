import json
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

url = "https://www.xwordinfo.com/JSON/Data.aspx"

my_headers = {
"Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Referer": "https://www.xwordinfo.com/JSON/",
"Host": "www.xwordinfo.com"
}

date = {"date":"9/11/2008"}

res = requests.get(url, headers=my_headers, params=date)
data=res.json()
print(data["answers"]["across"])