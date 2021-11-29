from copy import error
import json
from json import encoder
import requests
import html
from datetime import timedelta, date
import re
import sys
# These functions interact with the xword info API
# for more info see https://www.xwordinfo.com/JSON/


'''The very first NYT crossword was published on February 15, 1942.
Prior to September 11, 1950, NYT crosswords were published only on Sundays.
The pre-Shortz Era ended on November 20, 1993.'''


# generator function for dates
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def create_date(date_str):

    try:

        reg = "^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
        if re.match(reg, date_str):
            # split the date and create a list of ints
            dt_list = [int(x) for x in date_str.split("/")]
        else:
            print("Invalid date formatting")
            exit()

        dt = date(dt_list[0], dt_list[1], dt_list[2])
        return dt

    except Exception as e:
        raise SystemExit(e)


# list parameters in format YYYY, MM, DD
def xword_get_words(start_at, end_at=None):
    url = "https://www.xwordinfo.com/JSON/Data.aspx"

    # For whatever reason the API will not return data on a GET without the "Referer" header
    my_headers = {
    "Accept": "application/json",
    "Accept-Encoding": "utf-8",
    "Connection": "keep-alive",
    "Referer": "https://www.xwordinfo.com/JSON/",
    "Host": "www.xwordinfo.com"
    }
    try:
        start_dt = create_date(start_at)
        if end_at is not None:
            end_dt = create_date(end_at)
        else:
            end_dt = start_dt + timedelta(days=10)

        wordlist = [[] for x in range(20)]

        for dt in daterange(start_dt, end_dt):
            curr_dt = dt.strftime("%m/%d/%Y")


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

    #start=[2011, 12, 200]
    #end=[2012, 1, 2]
    start = sys.argv[1]

    my_list = xword_get_words(start)
    
    for wlen in my_list:
        for word in wlen:
            print(word)
    
if __name__ == "__main__":
    main()