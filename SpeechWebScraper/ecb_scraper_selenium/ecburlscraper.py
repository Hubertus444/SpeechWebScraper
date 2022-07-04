"""by Hubertus Mitschke created on 05/29/22"""
from datetime import date

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from cb_speech_scraper.urlscraper import URLScraper
from cb_speech_scraper.utils import progress_bar


class EcbURLScraper(URLScraper):
    """Scrape URLs and metadata from central bankers speeches from the BIS webpage"""

    def __init__(self, driver, first_index_year=1997, last_index_year=date.today().year,
                 index_url_str="https://www.ecb.europa.eu/press/key/date//{year}/html/index_include.en.html"):
        super().__init__(driver,
                         first_index=first_index_year,
                         last_index=last_index_year,
                         index_url_str=index_url_str)

    def scrape_url_basic_info(self) -> {str: {str: str}}:
        """
        Scrape URL and metadata of every single speech from every index page, indexed by year
        :return: dict with URLs as Keys and data of interest as dict as Values
        """
        for year in range(self.first_index, self.last_index + 1, 1):
            single_page_count = 0
            self.get_url(
                f"https://www.ecb.europa.eu/press/key/date//{year}/html/index_include.en.html"
            )
            date_element_rows, info_element_rows = self.__get_speech_table_rows()

            # Extract data from speech table rows
            for date_element, info_element in zip(date_element_rows, info_element_rows):
                self.url_dict.update(self.__extract_data_from_speech_row(date_element, info_element))
                single_page_count += 1
                progress_bar(single_page_count, len(date_element_rows), f"urls scraped from {year} page")

            self.increment_progress_count()
            progress_bar(self.running_num, self.last_index - self.first_index + 1,
                         f"scraping {year} index page (ECB)")

        return self.url_dict

    def __get_speech_table_rows(self) -> ([WebElement], [WebElement]):
        try:
            table = self.driver.find_element(By.TAG_NAME, 'body')
            return (self.__extract_date_elements_from_table(table),
                    self.__extract_info_elements_from_table(table))
        except NoSuchElementException:
            self.print_error_message("year index table body")

    def __extract_date_elements_from_table(self, table) -> [WebElement]:
        try:
            return table.find_elements(By.TAG_NAME, 'dt')
        except NoSuchElementException:
            self.print_error_message("year index dates dt")

    def __extract_info_elements_from_table(self, table) -> [WebElement]:
        try:
            return table.find_elements(By.TAG_NAME, 'dd')
        except NoSuchElementException:
            self.print_error_message("year index info dd")

    def __extract_data_from_speech_row(self, date_element, info_element):
        date_text = self.__extract_date_text_from_date_element(date_element)
        title = self.__extract_title_from_info_element(info_element)
        title_text = self.extract_title_text_from_title_element(title)
        url = self.extract_url_from_title_element(title)
        subtitle_text = self.extract_subtitle_from_info_element(info_element)
        language_text = self.__extract_language_from_info_element(info_element)
        return {
            url: {
                "url": url,
                "date": date_text,
                "title": title_text,
                "subtitle": subtitle_text,
                "language": language_text
            }
        }

    def __extract_date_text_from_date_element(self, date_element) -> str:
        try:
            return date_element.get_attribute('isodate')
        except NoSuchElementException:
            self.print_error_message("datetext")

    def __extract_title_from_info_element(self, info_element) -> WebElement:
        try:
            return info_element.find_element(By.CSS_SELECTOR, 'div.title')
        except NoSuchElementException:
            self.print_error_message("title")

    def extract_subtitle_from_info_element(self, info_element) -> str:
        try:
            return info_element.find_element(By.CSS_SELECTOR, 'div.subtitle').text
        except NoSuchElementException:
            self.print_error_message("subtitle")

    def __extract_language_from_info_element(self, info_element) -> str:
        try:
            return info_element.find_element(By.CSS_SELECTOR, 'span.offeredLanguage').text.strip()
        except NoSuchElementException:
            self.print_error_message("language")
