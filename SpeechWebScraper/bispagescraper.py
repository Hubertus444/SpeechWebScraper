"""by Hubertus Mitschke created on 05/29/22"""
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException
from cb_speech_scraper.pagescraper import PageScraper


class BisPageScraper(PageScraper):
    """Scrape central bankers speech data from a singular BIS web page representing a speech"""

    def __init__(self, driver, url, pdf_file_path, pdf_title="pdf_file.pdf"):
        super().__init__(driver, url, pdf_file_path, pdf_title)
        #self.pdf_file_path = "/Users/hubertus/Desktop/WebScraping PDFs/" + self.url.replace("https://www.bis.org/review/","").replace(".htm", ".pdf")
        #print(self.pdf_file_path)

    def scrape_page(self) -> {str: str}:
        """
        Scrape data from speech
        :return: dictionary mapping descriptors of the data of interest (str) to the data (str)
        """
        if self.url_contains_pdf(self.url):
            speech_text = self.scrape_pdf_file_from(self.url)
            author_text, subtitle_text, footnotes_text, add_pdf_page_content \
                = self.NA, self.NA, self.NA, self.NA
        else:
            author_text = self.__get_author()
            subtitle_text = self.__get_subtitle()
            speech_text = self.__get_speech()
            footnotes_text = self.__get_footnotes()
            add_pdf_page_content = self.__get_full_pdf_content()
        return {
            "author": author_text,
            "subtitle": subtitle_text,
            "speech": speech_text,
            "footnotes": footnotes_text,
            "url": self.url,
            "pdf": add_pdf_page_content
        }

    def __get_full_pdf_content(self) -> str:
        try:
            self.get_url(self.__extract_pdf_url())
            return self.scrape_pdf_file_from(self.driver.current_url, self.pdf_title)
        except InvalidArgumentException:
            self.print_error_message("could not retrieve valid url")

    def __get_author(self) -> str:
        try:
            return self.driver.find_element(By.CSS_SELECTOR, 'a.authorlnk').text.strip()

        except NoSuchElementException:
            self.print_error_message("author")

    def __get_subtitle(self) -> str:
        try:
            return self.driver.find_element(By.ID, "extratitle-div").text.strip()

        except NoSuchElementException:
            self.print_error_message("subtitle")

    def __get_speech(self) -> str:
        try:
            return self.driver.find_element(By.ID, "cmsContent").text.strip()

        except NoSuchElementException:
            self.print_error_message("speech")

    def __get_footnotes(self) -> [str]:
        try:
            footnotes_elements = self.driver.find_elements(By.CLASS_NAME, "footnote")
            return [footnote.text.strip() for footnote in footnotes_elements]

        except NoSuchElementException:
            self.print_error_message("footnotes")

    def __extract_pdf_url(self) -> str:
        try:
            return self.driver.find_element(By.CSS_SELECTOR, 'a.pdftitle_link').get_attribute("href")
        except NoSuchElementException:
            self.print_error_message("pdf-title-link")
