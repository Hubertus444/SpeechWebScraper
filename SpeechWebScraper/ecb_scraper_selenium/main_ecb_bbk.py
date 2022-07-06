"""
by Hubertus Mitschke created on 05/29/22

main file to scrape central bankers speech data from ECB
"""

from selenium import webdriver

from cb_speech_scraper.utils import progress_bar
from ecb_scraper_selenium.ecbpagescraper import EcbPageScraper
from ecb_scraper_selenium.ecburlscraper import EcbURLScraper
from cb_speech_scraper.timer import Timer
from cb_speech_scraper.data_wrangling import save_data_dict_to_csv, open_data_dict_from_csv
from cb_speech_scraper.utils import save_data_to_json, open_json_to_data


def run():

    SCRAPE_URLS = True
    IS_TEST_RUN = True
    # if test, which year:
    YEAR = 1997  # 2009


    TEST = "_test" if IS_TEST_RUN else ""
    ECB_FOLDER = "ecb_scraper_selenium/"
    #TODO: change PDF File Path to R:
    PDF_FILE_PATH = ECB_FOLDER + "pdf_files/file.pdf"
    #TODO: change Data File Path to R:
    COMPLETE_DATA_SAVE_PATH = ECB_FOLDER + f"data/ecb_speech{TEST}.csv"
    URL_SAVE_PATH = ECB_FOLDER + r"data/"
    URL_CSV_FILENAME = f"ecb_url{TEST}.csv"
    URL_JSON_FILENAME = f"ecb_url{TEST}.json"
    COMPLETE_DATA_JSON_SAVE_PATH = ECB_FOLDER + f"data/ecb_speech{TEST}.json"


    driver = webdriver.Chrome()
    #driver = webdriver.Edge()
    driver.minimize_window()

    if SCRAPE_URLS:
        if IS_TEST_RUN:
            scraper = EcbURLScraper(driver, first_index_year=YEAR, last_index_year=YEAR)
        else:
            scraper = EcbURLScraper(driver=driver)

        scraper.scrape_url_basic_info()
        data = scraper.url_dict

    for url, _ in data.items():
        scraper = EcbPageScraper(driver=driver, url=url, pdf_file_path=PDF_FILE_PATH)
        data[url].update(scraper.data_dict)

    driver.quit()

    save_data_dict_to_csv(data, COMPLETE_DATA_SAVE_PATH)
    #save_data_to_json(data, COMPLETE_DATA_JSON_SAVE_PATH)

if __name__ == "__main__":
    run()