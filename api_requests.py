import json
from json import encoder
import requests
import html
from datetime import timedelta, date

# generator function for dates
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

# list parameters in format YYYY, MM, DD
def xword_get(start_list, end_list):
    url = "https://www.xwordinfo.com/JSON/Data.aspx"

    # For whatever reason the API will not return data on a GET without the "Referer" header
    my_headers = {
    "Accept": "application/json",
    "Accept-Encoding": "utf-8",
    "Connection": "keep-alive",
    "Referer": "https://www.xwordinfo.com/JSON/",
    "Host": "www.xwordinfo.com"
    }

    start_dt = date(start_list[0], start_list[1], start_list[2])
    end_dt = date(end_list[0], end_list[1], end_list[2])

    wordlist = [[] for x in range(20)]

    for dt in daterange(start_dt, end_dt):
        curr_dt = dt.strftime("%m/%d/%Y")

        try:
            res = requests.get(url, headers=my_headers, params="date="+curr_dt)
            res.encoding='utf-8'
            data=res.json(encoding='utf-8')

            for x in range(len(data["answers"]["across"])):
                # the api returns escaped character and numbers before the answers so split on that and take second element
                word = html.unescape(data["answers"]["across"][x])
                clue = html.unescape(data["clues"]["across"][x]).split(". ")[1]
                wordlist[len(word.strip())-2].append((word.strip().lower(),clue.strip()))

            for x in range(len(data["answers"]["down"])):
                word=html.unescape(data["answers"]["down"][x])
                clue=html.unescape(data["clues"]["down"][x]).split(". ")[1]
                wordlist[len(word.strip())-2].append((word.strip().lower(),clue.strip()))

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    return wordlist

# main for testing
def main():

    start=[2019, 12, 20]
    end=[2020, 1, 2]

    my_list = xword_get(start, end)
    
    for wlen in my_list:
        for word in wlen:
            print(word)

if __name__ == "__main__":
    main()