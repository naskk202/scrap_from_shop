from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

opts = Options()
opts.add_argument("headless")
driver = webdriver.Chrome(options=opts)
driver.get("https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99")
time.sleep(3)


def cook_soup():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


soup = cook_soup()

info = {
    "name": "",
    "price": 0,
    "color": "",
    "size": []
}

name = soup.find_all("h1", {"itemprop": "name"})
info["name"] = name[0].text

price = soup.find_all("span", {"class": "product-sale product-sale--discount"})
selected_price = price[0].text
info["price"] = selected_price.split(".", 1)[1]

color = soup.find_all("div", {"class": "color-container color-container--selected"})
selected_color = color[0].attrs["aria-label"]
info["color"] = selected_color.split()[0]

size = soup.find_all("div", {"class", "selector"})
spans = size[0].find_all("span")

for span in spans[1:]:
    info["size"].append(span.attrs["data-size"])

for k, v in info.items():
    print(k, v)

with open("data.json", "w") as f:
    app = json.dump(info, f)
