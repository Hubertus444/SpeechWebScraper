"""
by Hubertus Mitschke created on 05/29/22

main file to scrape central bankers speech data from ECB
"""
import csv

from ecb_scraper_selenium.trash.ecbspeechscraper import *
from ecbpagescraper import EcbPageScraper
from ecburlscraper import EcbURLScraper

PDF_FILE_PATH = "pdf_files/file.pdf"


def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '#' * int(percent) + '-' * (100 - int(percent))
    # print(f"\r|{bar}| {percent:.2f}%", end="\r")
    print(f"\n{progress} of {total} |{bar}| {percent:.2f}%", end="\n")


counter = 0
calls = 0
fails = 0
pdfs = 0

SCRAPE_URLS = True
TEST_RUN = True

YEAR = 2004  # 2009#2004
TEST = "test" if TEST_RUN else ""
save_data_name = f"data/data2{TEST}.csv"
csv_save_name = f"urls_5{TEST}.csv"

s = "https://www.ecb.europa.eu/press/key/date/2004/html/sp040621.de.pdf"
if ".pdf" in s:
    print("YES")

# sys.exit(0)

start = time.time()

driver = webdriver.Safari()

if SCRAPE_URLS:

    if TEST_RUN:
        scraper = EcbURLScraper(driver, first_index_year=YEAR, last_index_year=YEAR)
    else:
        scraper = EcbURLScraper(driver=driver)

    scraper.scrape_url_basic_info()
    data = scraper.url_dict
    urls = data.keys()

    len_of_dict = len(data)

    with open(csv_save_name, 'w') as f:
        wr = csv.writer(f)
        wr.writerow(urls)

    print(urls)
    print(data)


# sys.exit(0)
else:
    data = {}
    with open(csv_save_name, newline='') as f:
        reader = csv.reader(f)
        urls = list(reader)[0]

    print(urls)
    len_of_dict = len(urls)

# for url, _ in data.items():
for url in urls:
    scraper = EcbPageScraper(driver=driver, url=url, pdf_file_path=PDF_FILE_PATH)
    if ".pdf" in scraper.url:
        pdfs += 1

    counter += 1
    progress_bar(counter, len_of_dict)
    calls += 7
    fails += scraper.fails

driver.quit()

end = time.time()

print("Fails:", fails, "Success:", calls - fails, "Total:", calls)
print(f"Total data: {len_of_dict}. PDFs: {pdfs}.")
timer = end - start
print(f"Total time: {timer // 60 // 60}h {timer // 60 % 60}min {timer % 60 % 60}sec")

df = pd.DataFrame(data)
df.to_csv(save_data_name)
