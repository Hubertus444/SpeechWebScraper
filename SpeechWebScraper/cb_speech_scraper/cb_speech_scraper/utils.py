"""by Hubertus Mitschke created on 05/29/22"""
import json

def save_data_to_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def open_json_to_data(path):
    with open(path, 'r') as f:
        return json.load(f)

def progress_bar(progress, total, task_description="", type='n', bar_type='❚') -> None:
    """
    Print a progress bar reflecting the degree of completion
    :param progress: int, the progress made so far
    :param total: int, the total amount of work to be done
    :param task_description: str, optional, describes the task measured
    :param type: str, 'n': prints a progress bar every newline, 'r': prints it in the same line
    :return: None
    """
    bar_type = '#'
    percent = min(100 * (progress / float(total)), 100)
    bar = bar_type * int(percent) + '-' * (100 - int(percent))
    # print(f"\r|{bar}| {percent:.2f}%", end="\r")
    task_description += ":" if task_description else ""
    if type == 'n':
        print(f"\n{task_description} {progress} of {total} |{bar}| {percent:.2f}%", end="\n")
    else:
        print(f"\r{task_description} {progress} of {total} |{bar}| {percent:.2f}%", end="\r")


TEST = "_test"
COMPLETE_DATA_JSON_SAVE_PATH = r"/Users/hubertus/Documents/0_Bachelor Computation and Cognition/71/SpeechWebScraper/ecb_scraper_selenium/data/ecb_speech.json"
data = open_json_to_data((COMPLETE_DATA_JSON_SAVE_PATH))
print(data[r'https://www.ecb.europa.eu/press/key/date/2022/html/ecb.sp220614~67eda62c44.en.html'])
for k, v in data.items():
    print("KEY", k, "VALUE", v)
    for subk, subv in v.items():
        print("\n\n\nNEXT")
        print(subk, ":", subv)
    break

print(len(data))