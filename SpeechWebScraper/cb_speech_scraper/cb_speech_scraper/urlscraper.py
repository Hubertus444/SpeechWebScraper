"""by Hubertus Mitschke created on 05/29/22"""
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from cb_speech_scraper.speechscraper import SpeechScraper


class URLScraper(SpeechScraper):
    """Base class to scrape urls and basic info from index pages"""

    def __init__(self, driver, first_index, index_url_str, last_index=None, waiting_time=30):
        super().__init__(driver)
        self.first_index = first_index
        self.last_index = last_index
        self.index_url_str = index_url_str
        self.waiting_time = waiting_time

        self.url_dict = {}
        self.running_num = 0

    def increment_progress_count(self) -> None:
        self.running_num += 1

    def extract_url_from_title_element(self, title) -> str:
        try:
            return title.find_element(By.TAG_NAME, 'a').get_attribute('href')

        except NoSuchElementException:
            self.print_error_message("url from title")

    def extract_title_text_from_title_element(self, title) -> str:
        try:
            return title.text.strip()

        except TypeError:
            self.print_error_message("no text in title")
