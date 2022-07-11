"""by Hubertus Mitschke created on 05/29/22"""
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from cb_speech_scraper.urlscraper import URLScraper
from cb_speech_scraper.utils import progress_bar


class BisURLScraper(URLScraper):
    """Scrape URLs and metadata from central bankers speeches from the BIS webpage"""

    def __init__(self, driver, first_index_page=1, last_index_page=None, waiting_time=30,
                 index_url_str="https://www.bis.org/cbspeeches/index.htm?cbspeeches_page={page}&cbspeeches=ZnJvbT0mdGlsbD0mb2JqaWQ9Y2JzcGVlY2hlcyZwYWdlPS0xJnBhZ2luZ19sZW5ndGg9MjUmc29ydF9saXN0PWRhdGVfZGVzYyZ0aGVtZT1jYnNwZWVjaGVzJm1sPWZhbHNlJm1sdXJsPSZlbXB0eWxpc3R0ZXh0PQ%253D%253D"):
        super().__init__(driver,
                         first_index=first_index_page,
                         last_index=last_index_page,
                         index_url_str=index_url_str,
                         waiting_time=waiting_time)

        self.last_index = (self.__find_num_last_index_page()
                           if last_index_page is None
                           else last_index_page)
        self.get_url('https://www.bis.org/cbspeeches/index.htm?cbspeeches_page=1&cbspeeches=ZnJvbT0mdGlsbD0mb2JqaWQ9Y2JzcGVlY2hlcyZwYWdlPS0xJnBhZ2luZ19sZW5ndGg9MjUmc29ydF9saXN0PWRhdGVfZGVzYyZ0aGVtZT1jYnNwZWVjaGVzJm1sPWZhbHNlJm1sdXJsPSZlbXB0eWxpc3R0ZXh0PQ%253D%253D')
        self.SPEECHES_PER_PAGE = int(
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cbspeeches_list"]/div/div[1]/div[2]/b')
                )
            ).text.replace(',', '')
        )#25

    def scrape_url_basic_info(self) -> {str: {str: str}}:
        """
        Scrape URL and metadata of every single speech from every index page, indexed by page number
        :return: dict with URLs as Keys and data of interest as dict as Values
        """
        for page in range(self.first_index, self.last_index + 1, 1):
            self.get_url(
                self.index_url_str.format(page=page)
            )

            # Extract data from speech table rows
            speech_table_rows = self.__get_speech_table_rows()
            for speech_row in speech_table_rows:
                self.url_dict.update(self.__extract_data_from_speech_row(speech_row))

                self.increment_progress_count()
                progress_bar(self.running_num, self.SPEECHES_PER_PAGE, "scraping URLs from BIS")

        return self.url_dict

    def __get_speech_table_rows(self) -> [WebElement]:
        try:
            speech_table = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cbspeeches_list"]')
                )
            )
            return WebDriverWait(speech_table, self.waiting_time).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'item')
                )
            )
        except NoSuchElementException:
            self.print_error_message("speech table rows")

    def __extract_data_from_speech_row(self, speech_row) -> {str: {str: str}}:
        date_text = self.__extract_date_text_from_speech_row(speech_row)
        title = self.__extract_title_from_speech_row(speech_row)
        title_text = self.extract_title_text_from_title_element(title)
        url = self.extract_url_from_title_element(title)
        return {
            url: {
                "date": date_text,
                "title": title_text,
                "url": url
            }
        }

    def __extract_date_text_from_speech_row(self, speech_row) -> str:
        try:
            return speech_row.find_element(By.CLASS_NAME, "item_date").text.strip()

        except NoSuchElementException:
            self.print_error_message("publication date")

    def __extract_title_from_speech_row(self, speech_row) -> WebElement:
        try:
            return speech_row.find_element(By.CLASS_NAME, "title")

        except NoSuchElementException:
            self.print_error_message("title-element")

    def __find_num_last_index_page(self) -> int:
        try:
            self.get_url(
                self.index_url_str.format(page=self.first_index)
            )
            last_page_str = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cbspeeches_list"]/div/div[2]/nav/div/div[2]/div/div[2]/span')
                )
            ).text
            return int(last_page_str.split()[-1])

        except NoSuchElementException:
            self.print_error_message("Index of Last Page")
