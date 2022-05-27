"""by Hubertus Mitschke created on 05/29/22"""
from abc import ABC

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class SpeechScraper(ABC):
    """Base class with basic functionality of a speech scraper"""
    def __init__(self, driver, waiting_time=30):
        self.driver = driver if driver is not None else webdriver.Safari()
        self.fails = 0
        self.wait = WebDriverWait(self.driver, waiting_time)

    def get_url(self, url) -> None:
        self.driver.get(url)

    def get_init_url(self) -> None:
        self.driver.get(self.url)

    def quit_driver(self) -> None:
        self.driver.quit()

    def print_error_message(self, error_element) -> None:
        """
        Print an error message for errors from scraping elements
        :param error_element: str, naming the errorneous element
        :return: None
        """
        print(f"Failed for: {self.url}, Element: {error_element}.")
        self.fails += 1
