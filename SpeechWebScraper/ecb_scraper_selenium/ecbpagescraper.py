"""by Hubertus Mitschke created on 05/29/22"""
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from cb_speech_scraper.pagescraper import PageScraper


class EcbPageScraper(PageScraper):
    """Scrape central bankers speech data from a single ECB web page representing a single speech"""

    def __init__(self, driver, url, pdf_file_path):
        super().__init__(driver, url, pdf_file_path)
        self.data_dict = self.scrape_page()

    def scrape_page(self) -> dict:
        """
        Scrape data from speech
        :return: dictionary mapping descriptors of the data of interest (str) to the data (str), ({int: str}), ([str])
        """
        if (self.url_contains_pdf(self.url)
                or self.url_contains_pdf(self.driver.current_url)):
            speech_text = self.scrape_pdf_file_from(self.url)
            classification = "slideshow"
            title_text, subtitle_text, location_date \
                = self.NA, self.NA, self.NA
            footnotes_dict, related_topics_list = {}, []
        else:
            title = self.__extract_title_element()

            classification = self.__get_classification_from_title(title)
            title_text = self.__get_title_text_from_title(title)

            section_list = self.__extract_section_list()

            speech_text = self.__get_speech_text_from_section_list(section_list)
            subtitle_text = self.__get_subtitle_from_section_list(section_list)
            location_date = self.__get_location_date_from_section_list(section_list)

            footnotes_dict = self.__get_footnotes_dict()
            related_topics_list = self.__get_related_topics()

        # update self.data_dict instead in main
        # self.data_dict = { data here }
        return {
            "p_subtitle": subtitle_text,
            "speech": speech_text,
            "footnotes": footnotes_dict,
            "p_url": self.url,
            "p_title": title_text,
            "related_topics": related_topics_list,
            "locdate": location_date,
            "classification": classification
        }

    def __get_classification_from_title(self, title) -> str:
        '''

        :param title:
        :return: classification
        '''
        try:
            return title.find_element(By.TAG_NAME, 'ul').text
        except (NoSuchElementException, AttributeError):
            self.print_error_message("classification")

    def __get_title_text_from_title(self, title) -> str:
        '''

        :param title:
        :return:
        '''

        try:
            return title.find_element(By.TAG_NAME, 'h1').text
        except (NoSuchElementException, AttributeError):
            self.print_error_message("title")

    def __extract_section_list(self) -> [WebElement]:
        try:
            sections = self.driver.find_elements(By.CSS_SELECTOR, 'div.section')[2:]
            if not sections:
                try:
                    sections = [self.driver.find_element(By.TAG_NAME, 'article')]
                    print("OLD PAGE LAYOUT")
                    return sections
                except NoSuchElementException:
                    self.print_error_message("no old page layout speech")
            else:
                return sections
        except NoSuchElementException:
            self.print_error_message("no sections at all")

    def __get_speech_text_from_section_list(self, section_list) -> str:
        try:
            speech = ""
            for section in section_list:
                speech += section.text.strip() + '\n'

            return speech
        except TypeError:
            self.print_error_message("section_list is NoneType")

    def __get_subtitle_from_section_list(self, section_list) -> str:
        try:
            section = section_list[0]
            return section.find_element(By.CSS_SELECTOR, 'h2.ecb-pressContentSubtitle').text
        except (NoSuchElementException, TypeError):
            self.print_error_message("subtitle")

    def __get_location_date_from_section_list(self, section_list) -> str:
        try:
            section = section_list[0]
            return section.find_element(By.CSS_SELECTOR, 'p.ecb-publicationDate').text
        except (NoSuchElementException, TypeError):
            self.print_error_message("locdate")

    def __get_footnotes_dict(self) -> {int: str}:
        '''

        :return:
        '''
        footnotes_dict = {}

        try:
            m_footnotes_list = self.driver.find_element(By.CSS_SELECTOR, 'div.footnotes') \
                .find_elements(By.TAG_NAME, 'li')

            for i, ft in enumerate(m_footnotes_list):
                footnotes_dict[i + 1] = ft.text

        except NoSuchElementException:
            self.print_error_message("footnotes")

        return footnotes_dict

    def __get_related_topics(self) -> [str]:
        '''

        :return:
        '''
        try:
            m_relatedtopics_list = self.driver.find_element(By.CSS_SELECTOR, 'div.related-topics') \
                .find_elements(By.TAG_NAME, 'a')
            return [topic.text for topic in m_relatedtopics_list]

        except NoSuchElementException:
            self.print_error_message("related topics")

    def __extract_title_element(self) -> WebElement:
        try:
            return self.driver.find_element(By.CSS_SELECTOR, 'div.title')
        except NoSuchElementException:
            self.print_error_message("title element")

    def consent_to_cookies(self) -> None:
        button = self.driver.find_element(By.XPATH, '//*[@id="cookieConsent"]/div[1]/div/a[1]')
        button.click()
