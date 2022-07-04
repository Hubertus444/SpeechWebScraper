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
    timer = Timer()
    timer.start_timer()

    SCRAPE_URLS = True
    IS_TEST_RUN = True
    # if test, which year:
    YEAR = 1997  # 2009

    counter = 0
    calls = 0
    fails = 0

    TEST = "_test" if IS_TEST_RUN else ""
    PDF_FILE_PATH = "ecb_scraper_selenium/pdf_files/file.pdf"
    COMPLETE_DATA_SAVE_PATH = f"data/ecb_speech{TEST}.csv"
    URL_SAVE_PATH = r"ecb_scraper_selenium/data/"
    URL_CSV_FILENAME = f"ecb_url{TEST}.csv"
    URL_JSON_FILENAME = f"ecb_url{TEST}.json"
    COMPLETE_DATA_JSON_SAVE_PATH = f"data/ecb_speech{TEST}.json"



    #driver = webdriver.Safari()
    driver = webdriver.Chrome()
    driver.minimize_window()

    url_timer = Timer()
    url_timer.start_timer()

    if SCRAPE_URLS:

        if IS_TEST_RUN:
            scraper = EcbURLScraper(driver, first_index_year=YEAR, last_index_year=YEAR)
        else:
            scraper = EcbURLScraper(driver=driver)

        scraper.scrape_url_basic_info()
        data = scraper.url_dict
        save_data_dict_to_csv(data, URL_SAVE_PATH + URL_CSV_FILENAME)
        save_data_to_json(data, URL_SAVE_PATH + URL_JSON_FILENAME)

    data = open_data_dict_from_csv(URL_SAVE_PATH + URL_CSV_FILENAME)
    len_of_dict = len(data)

    url_timer.stop_timer()
    pages_timer = Timer()
    pages_timer.start_timer()

    for url, _ in data.items():
        scraper = EcbPageScraper(driver=driver, url=url, pdf_file_path=PDF_FILE_PATH)
        data[url].update(scraper.data_dict)

        counter += 1
        calls += 7
        fails += scraper.fails
        progress_bar(counter, len_of_dict)

    driver.quit()

    print("Fails:", fails, "Success:", calls - fails, "Total:", calls)
    print(f"Total data: {len_of_dict}")

    save_data_dict_to_csv(data, COMPLETE_DATA_SAVE_PATH)
    save_data_to_json(data, COMPLETE_DATA_JSON_SAVE_PATH)

    pages_timer.stop_timer()
    timer.stop_timer()


    print(f"Total PAGE fails: {fails}.")
    timer.print_timing_info(timing_description="Total scraping process")
    url_timer.print_timing_info(timing_description="URL scraping process")
    pages_timer.print_timing_info(timing_description="Pages scraping process")

if __name__ == "__main__":
    run()