"""
by Hubertus Mitschke created on 05/29/22

main file to scrape central bankers speech data from BIS
"""
from selenium import webdriver

from bispagescraper import BisPageScraper
from bisurlscraper import BisURLScraper
from cb_speech_scraper.timer import Timer
from cb_speech_scraper.utils import progress_bar, save_data_to_json, open_json_to_data
import pandas as pd
from cb_speech_scraper.data_wrangling import save_data_dict_to_csv, open_data_dict_from_csv

def main():
    # Setup timer
    timer = Timer()
    url_timer = Timer()
    pages_timer = Timer()

    # Setup settings for running scraper
    SCRAPE_URLS = True
    IS_TEST_RUN = True
    PAGE = 3  # if test, which page:

    # General setups
    fails = 0
    TEST = "_test" if IS_TEST_RUN else ""
    R_DIR = r"R:\Zentrale\Projekte\Daten\Webscraping\Webscraping Reden SilkCentral\\"
    PDF_FOLDER = r"\ECB\pdf\\"
    DATA_FOLDER = r"\ECB\data\\"
    PDF_FILE_PATH = R_DIR + PDF_FOLDER  # file.pdf
    DATA_CSV_SAVE_PATH = R_DIR + DATA_FOLDER + f"ecb_speech{TEST}.csv"
    DATA_JSON_SAVE_PATH = R_DIR + DATA_FOLDER + f"ecb_speech{TEST}.json"
    URL_CSV_SAVE_PATH = R_DIR + DATA_FOLDER + f"ecb_url{TEST}.csv"
    URL_JSON_SAVE_PATH = R_DIR + DATA_FOLDER + f"ecb_url{TEST}.json"

    # Starting up the driver
    driver = webdriver.Edge(executable_path=r"C:\Workspace\Selenium\msedgedriver.exe")

    #######################
    # OVERALL Scraping Process
    timer.start_timer()
    # START

    #######################
    # URL Scraping Process
    url_timer.start_timer()
    # START
    if SCRAPE_URLS:
        if IS_TEST_RUN:
            url_scraper = BisURLScraper(driver=driver, last_index_page=PAGE)
        else:
            url_scraper = BisURLScraper(driver=driver)
        data = url_scraper.scrape_url_basic_info()

        save_data_dict_to_csv(data, URL_CSV_SAVE_PATH)
        save_data_to_json(data, URL_JSON_SAVE_PATH)

    # END
    url_timer.stop_timer()
    url_timer.print_timing_info("url scraping")
    # URL Scraping Process
    #######################
    data = open_json_to_data(DATA_JSON_SAVE_PATH)

    #######################
    # PAGES Scraping Process
    pages_timer.start_timer()
    # START

    # General initializations
    SPEECHES_SCRAPED_LAST_TIME = 0
    END_AT = 18_000
    speeches_scraped_so_far = 0
    num_of_urls = len(data)

    # Testing Suite
    TEST_RUN_SPEECHES_NUM = 25 * PAGE + 1
    test_counter = 0

    for url, values in data.items():
        test_counter += 1
        speeches_scraped_so_far += 1

        if speeches_scraped_so_far < SPEECHES_SCRAPED_LAST_TIME + 1:
            continue
        if speeches_scraped_so_far > END_AT:
            break
        if IS_TEST_RUN:
            if test_counter > TEST_RUN_SPEECHES_NUM:
                break
        #try:
        page_scraper = BisPageScraper(
                driver,
                url,
                pdf_file_path=PDF_FILE_PATH,
                pdf_title=values["title"]+".pdf")
        #except Exception as e:
        #    print(e)

        progress_bar(speeches_scraped_so_far, num_of_urls, f"{values['date']} - scraping speeches")

        data[url].update(page_scraper.scrape_page())
        fails += page_scraper.fails

        # save every 500 speeches:
        if test_counter % 500 == 0 or speeches_scraped_so_far == num_of_urls:
            complete_data_save_file_path =  R_DIR + DATA_FOLDER + f"bis_speech{TEST}_{SPEECHES_SCRAPED_LAST_TIME}_up_to_{speeches_scraped_so_far}.json"
            save_data_to_json(data_dict=data, save_file_path=complete_data_save_file_path)

    driver.quit()

    # END
    pages_timer.stop_timer()
    # PAGES Scraping Process
    #######################

    # final save
    save_data_dict_to_csv(data_dict=data, save_file_path=DATA_CSV_SAVE_PATH)
    # END
    timer.stop_timer()

    if SCRAPE_URLS:
        print(f"URL fails: {url_scraper.fails}. ", end="")
    print(f"Total PAGE fails: {fails}.")
    timer.print_timing_info(timing_description="Total scraping process")
    url_timer.print_timing_info(timing_description="URL scraping process")
    pages_timer.print_timing_info(timing_description="Pages scraping process")
    # OVERALL Scraping Process
    #######################

if __name__ == "__main__":
    main()

