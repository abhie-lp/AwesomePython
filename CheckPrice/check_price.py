import requests
from bs4 import BeautifulSoup as BS
from sys import argv
import csv
from datetime import datetime
from os import path
from re import compile


class Check_Price():
    #Columns for the resulting ouptut to csv file
    COLUMNS = ["DATE", "TITLE", "PRICE", "URL"]

    # make an empty file if it isn't present
    def __init__(self):
        if not path.isfile("./prices.csv"):                     # If file is not present
            with open("prices.csv", "w") as f:
                self.file_w = csv.DictWriter(f, self.COLUMNS)
                self.file_w.writeheader()                       # Only write the column names

    # Check the command line arguments whether it is a text file or url
    def check_arguments(self):
        if len(argv) == 2 and argv[1].endswith(".txt"):
            return "file"
        else:
            return "url"

    # Load the urls either from a text file or command line
    def load_urls(self):
        urls = []
        if self.check_arguments() == "file":
            file_name = argv[1]
            with open(file_name) as f:
                for url in f:
                    urls.append(url.strip())
            return urls
        else:
            return argv[1:]

    # Download the page using request
    def download_page(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.104"}
        page = requests.get(url, headers=headers)
        return page

    # Start scraping and return title, price
    def scrape(self, page):
        soup = BS(page, "lxml")                                             # Build the BeautifulSoup object
        title_ele = soup.find("div", id="title_feature_div")                # Title block
        title = title_ele.find("span", id="productTitle").text.strip()      # Title of the product
        price_ele = soup.find("div", id="unifiedPrice_feature_div")         # Price block
        price = price_ele.find("span", id=compile(r"priceblock_")).text.strip()     # Price of product
        return title, price

    # Write the output to a file inorder to check the previous prices
    def write_to_file(self, title, price, url):
        with open("prices.csv", "a") as f:
            file_w = csv.DictWriter(f, self.COLUMNS)
            # Write the data in their respective columns
            file_w.writerow({"DATE": str(datetime.now().date()), "TITLE": title, "PRICE": price, "URL": url})

    # Call all the above functions
    def main(self):
        urls = self.load_urls()
        for url in urls:
            print("current URL:", url)
            page = self.download_page(url)
            if page.status_code == 200:                         # If requests.get was unable to fetch url data
                title, price = self.scrape(page.text)
                self.write_to_file(title, price, url)
            else:
                print("URL not available")


if __name__ == "__main__":
    obj = Check_Price()
    obj.main()
