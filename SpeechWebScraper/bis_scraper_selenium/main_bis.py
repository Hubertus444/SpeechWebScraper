"""
by Hubertus Mitschke created on 05/29/22

main file to scrape central bankers speech data from BIS
"""
from selenium import webdriver

from bispagescraper import BisPageScraper
from bisurlscraper import BisURLScraper
from timer import Timer
from utils import progress_bar

timer = Timer()

driver = webdriver.Safari()

PDF_FILE_PATH = "pdf_files/file.pdf"

timer.start_timer()
scraper = BisURLScraper(driver=driver, last_index_page=2)

data = scraper.scrape_url_basic_info()

progress = 0
total = len(data)

for url, _ in data.items():
    scraper2 = BisPageScraper(
        driver,
        url,
        pdf_file_path=PDF_FILE_PATH)
    progress += 1
    progress_bar(progress, total, "scraping speeches")
    data[url].update(scraper2.scrape_page())

# print(data['https://www.bis.org/review/r220511a.htm'])
# print(data['https://www.bis.org/review/r220511a.htm']["pdf"])

driver.quit()

timer.stop_timer()
print(timer.time_elapsed)
print(scraper.fails, scraper2.fails)
timer.print_timing_info()
