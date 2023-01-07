import requests
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup as bs 
import calendar
import random
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

for year in range(2017,2024):
    for month in range(1,13):
        month = "{:02d}".format(month)

        for page_number in range(1,10000):

            page_link = f"https://bankurapolice.org/{year}/{month}/page/{page_number}/?post_type=fir"

            try:
                resp = requests.get(page_link, headers=headers)
            except:
                try:
                    resp = requests.get(page_link, headers=headers)
                except:
                    continue

            if resp.status_code !=200:
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
                    file = requests.get(pdf_link, timeout=5, headers=headers)
                except:
                    continue

                
                filename.write_bytes(file.content)
                print("\033[32m"+str(filename) + "\tdownloaded")