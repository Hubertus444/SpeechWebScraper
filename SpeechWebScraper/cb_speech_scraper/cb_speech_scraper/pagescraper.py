"""by Hubertus Mitschke created on 05/29/22"""
import time
import urllib

import selenium.common.exceptions
from selenium import webdriver
from bs4 import BeautifulSoup
from tika import parser

from cb_speech_scraper.speechscraper import SpeechScraper


class PageScraper(SpeechScraper):
    """Base class PageScraper to scrape a single web page"""

    def __init__(self, driver, url, pdf_file_path):
        super().__init__(driver)
        self.url = url
        self.pdf_file_path = pdf_file_path
        self.fails = 0
        self.NA = "na"
        self.data_dict = {}

        self.get_url(url)

    def scrape_pdf_file_from(self, url) -> str:
        """
        Download and extract main text from pdf

        :param url: str, url of the pdf to scrape
        :return: str, main text of pdf
        """
        try:
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
        except TimeoutError as e:
            self.print_error_message("timed out of url error")
            print(e)
            return "NO PDF RETRIEVED"
        except urllib.error.URLError as e:
            self.print_error_message("some URL timed out")
            print(e)
            return "NO PDF RETRIEVED"

        with open(self.pdf_file_path, "wb") as f:
            f.write(response.read())

        raw = parser.from_file(self.pdf_file_path, xmlContent=True)['content']
        # raw = parser.from_file(url, xmlContent=True)['content']

        data = BeautifulSoup(raw, 'lxml')
        # TODO: maybe extract data as list of single paragraphs to preserve the lxml structure?
        pdf_content = data.find_all("div", {"class": "page"})
        return "".join([div.text for div in pdf_content])

    def url_contains_pdf(self, url) -> bool:
        return url[-3:] == "pdf"
