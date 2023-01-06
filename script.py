import requests
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup as bs 
import pandas as pd
import calendar
import random

for year in range(2018,2024):
    for month in range(1,13):
        month = "{:02d}".format(month)

        for page_number in range(1,10000):

            page_link = f"https://bankurapolice.org/{year}/{month}/page/{page_number}/?post_type=fir"

            try:
                resp = requests.get(page_link)
            except:
                try:
                    resp = requests.get(page_link)
                except:
                    continue
            # print(resp.status_code)

            if resp.status_code !=200:
                break
            
            soup = bs(resp.content, features="html.parser")
            divs = soup.find_all('div', class_="col-md-4")
            for a in divs:
                pdf_link = a.a['href']

                try:
                    filename = pdf_link[pdf_link.rfind('/')+1:]
                except:
                    filename = str(year) + str(month) + str(page_number) + str(random.randint(1,1000)) + ".pdf"

                try:
                    file = requests.get(pdf_link, timeout=5)
                except:
                    continue

                path = Path.cwd().joinpath("data", str(year), str(calendar.month_name[int(month)]))
                path.mkdir(parents=True, exist_ok=True)
                path.joinpath(filename).write_bytes(file.content)
                print(str(path) +"/"+ str(filename))












































# year, month, day
start_date = datetime(2020, 1, 1)
date= datetime(2020, 12, 31)

domain = "https://alipurduarpolice.org/"
url = "https://alipurduarpolice.org/fir.php"

headers = CaseInsensitiveDict()
headers["authority"] = "alipurduarpolice.org"
headers["path"] = "/fir.php"
headers["scheme"] = "https"
headers["accept-language"] = "en-GB,en;q=0.7"
headers["cache-control"] = "max-age=0"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["sec-ch-ua-mobile"] = "?0"
headers["sec-ch-ua-platform"] = "Linux"
headers["sec-fetch-dest"] = "document"
headers["sec-fetch-mode"] = "navigate"
headers["sec-fetch-site"] = "same-origin"
headers["sec-fetch-user"] = "?1"
headers["sec-gpc"] = "1"
headers["upgrade-insecure-requests"] = "1"
headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'

police_station ={
	"1": "Alipurduar",
	"2": "Falakata",
	"3": "Kumargram",
	"4": "Samuktala",
	"5": "Kalchini",
	"6": "Jaigaon",
	"7": "Madarihat",
	"8": "Birpara",
	"9": "Alipurduar Police Head Quarter",
	"10": "CI Office Kalchini",
	"11": "CI Office Birpara",
	"12": "ALIPURDUAR WOMEN PS",
	"13": "Cyber Crime Police Station"
}

#data = "start_date=10%2F01%2F2022&police_station=1&submit=Submit"
#month day year

excel_data = []
last_file_reached = False

print()
while (date>=start_date):

	print(date)

	month = date.month
	if month < 10:
		month = "0"+str(month)
	else:
		month = str(month)

	year = str(date.year)

	day = date.day
	if day < 10:
		day = "0"+str(day)
	else:
		day = str(day)

	for i in range(1,14):

		print(police_station[str(i)])

		data = "start_date="+month+"%2F"+day+"%2F"+year+"&police_station="+str(i)+"&submit=Submit"
		resp = requests.post(url, headers=headers, data=data)
		soup = bs(resp.content, features="html.parser")
		firs = soup.find_all("div", {"class": "con1"})

		for fir in firs:
			
			title = fir.find("h4").string
			section = fir.find("p").string
			try:
				intermediate_link = fir.find("a").get("href")
			except:
				fir_present = "FIR NOT UPLOADED ON SITE"
				excel_data.append({"title":title, "sections":section, "police station": police_station[str(i)] ,"FIR present": fir_present, "intermediate link": "NA", \
				"final link": "NA", "file name": ""})
				continue

			# if !last_file_reached and intermediate_link < "fir1.php?fir=10640":
			# 	last_file_reached = True
			response = requests.get(domain+intermediate_link+"&confirm=yes", headers=headers)
			k = response.content
			k = k.decode()
			k = k.replace("<SCRIPT LANGUAGE='JavaScript'>window.location.href='", "")
			k = k.replace("';</SCRIPT>","")

			final_link = domain+k
			response = requests.get(final_link, headers=headers)
			filename = k.replace('upload_image/download/', '')

			if response.status_code == 404:
				fir_present = "FIR MISSING FROM SERVER"
				filename = ""
				excel_data.append({"title":title, "sections":section, "police station": police_station[str(i)] ,"FIR present": fir_present, "intermediate link": domain+intermediate_link, \
				"final link": final_link, "file name": filename})
				continue

			fir_present = "YES"
			path = Path.cwd().joinpath(year, date.strftime("%B"), police_station[str(i)])
			path.mkdir(parents=True, exist_ok=True)
			path.joinpath(filename).write_bytes(response.content)

			excel_data.append({"title":title, "sections":section, "police station": police_station[str(i)] ,"FIR present": fir_present, "intermediate link": domain+intermediate_link, \
				"final link": final_link, "file name": filename})

			

	if date.day == datetime(2022, 1, 1).day:
		path = 	Path.cwd().joinpath(year, date.strftime("%B"))
		path.mkdir(parents=True, exist_ok=True)

		df = pd.DataFrame.from_dict(excel_data)
		df.to_excel(path.joinpath(date.strftime("%B")+ " "+ year +".xslx"), index=False)
		excel_data = []

		# if last_file_reached:
		# 	print("last file reached")
		# 	break
	date = date-timedelta(days=1)