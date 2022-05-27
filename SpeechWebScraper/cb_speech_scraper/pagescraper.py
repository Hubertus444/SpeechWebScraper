"""by Hubertus Mitschke created on 05/29/22"""
import urllib

from bs4 import BeautifulSoup
from tika import parser

from speechscraper import SpeechScraper


class PageScraper(SpeechScraper):
    """Base class PageScraper to scrape a single web page"""

    def __init__(self, driver, url, pdf_file_path):
        super().__init__(driver)
        self.url = url
        self.pdf_file_path = pdf_file_path
        self.fails = 0
        self.get_init_url()
        self.NA = "na"

    def scrape_pdf_file_from(self, url) -> str:
        """
        Download and extract main text from pdf

        :param url: str, url of the pdf to scrape
        :return: str, main text of pdf
        """
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)

        with open(self.pdf_file_path, "wb") as f:
            f.write(response.read())

        raw = parser.from_file(self.pdf_file_path, xmlContent=True)['content']
        data = BeautifulSoup(raw, 'lxml')
        pdf_content = data.find_all("div", {"class": "page"})
        return "".join([div.text for div in pdf_content])

    def url_contains_pdf(self, url) -> bool:
        return url[-3:] == "pdf"
