from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.parkrun.com.au/special-events/"

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"}
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, "lxml")

res = soup.find_all("table", attrs={"id":"results"})

f = open("locations.csv", "w", newline='', encoding='utf-8-sig')
writer = csv.writer(f)

for i in range(1, len(res[0].contents)):
    writer.writerow([res[0].contents[i].find("a")["href"][27:-1]])
