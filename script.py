import requests
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup as bs 
import calendar
import random
import os
import time
from itertools import cycle


user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]
list_proxy = [ None,  'http://110.234.32.234:3128']
proxy_cycle = cycle(list_proxy)
proxy = next(proxy_cycle)

for year in range(2017,2024):
    for month in range(1,13):
        month = "{:02d}".format(month)

        for page_number in range(1,10000):

            page_link = f"https://bankurapolice.org/{year}/{month}/page/{page_number}/?post_type=fir"

            proxies = {
                "http": proxy,
                "https":proxy
            }

            try:
                resp = requests.get(page_link, headers={'User-Agent': random.choice(user_agents_list)},  proxies=proxies)
            except:
                try:
                    resp = requests.get(page_link, headers={'User-Agent': random.choice(user_agents_list)}, proxies=proxies)
                except:
                    continue
            
            if resp.status_code == 403:
                while(True):
                    print("\033[91m" + str(page_link) + "\t"+str(resp.status_code))
                    proxy = next(proxy_cycle)
                    print("\033[32m" + "Using proxy: "+ str(proxy))
                    resp = requests.get(page_link, headers={'User-Agent': random.choice(user_agents_list)}, proxies=proxies)
                    if resp.status_code == 403:
                        print("sleeping")
                        time.sleep(1000)
                    else:
                        break
                    

            if resp.status_code == 404:
                print("\033[91m" + str(page_link) + "\t"+str(resp.status_code))
                break
            
            soup = bs(resp.content, features="html.parser")
            divs = soup.find_all('div', class_="col-md-4")
            for a in divs:
                pdf_link = a.a['href']

                path = Path.cwd().joinpath("data", str(year), str(calendar.month_name[int(month)]))
                path.mkdir(parents=True, exist_ok=True)

                try:
                    filename =  path.joinpath(pdf_link[pdf_link.rfind('/')+1:])
                except:
                    filename = path.joinpath(str(year) + str(month) + str(page_number) + str(random.randint(1,1000)) + ".pdf")

                if os.path.exists(filename):
                    print("\033[93m" + str(filename) + "\tfile already present")
                    continue

                try:
                    file = requests.get(pdf_link, timeout=5, headers={'User-Agent': random.choice(user_agents_list)})
                except:
                    continue

                
                filename.write_bytes(file.content)
                print("\033[32m"+str(filename) + "\tdownloaded")