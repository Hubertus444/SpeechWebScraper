"""by Hubertus Mitschke created on 05/29/22"""
def progress_bar(progress, total, task_description="", type='n') -> None:
    """
    Print a progress bar reflecting the degree of completion
    :param progress: int, the progress made so far
    :param total: int, the total amount of work to be done
    :param task_description: str, optional, describes the task measured
    :param type: str, 'n': prints a progress bar every newline, 'r': prints it in the same line
    :return: None
    """
    percent = min(100 * (progress / float(total)), 100)
    bar = '#' * int(percent) + '-' * (100 - int(percent))
    # print(f"\r|{bar}| {percent:.2f}%", end="\r")
    task_description += ":" if task_description else ""
    if type == 'n':
        print(f"\n{task_description} {progress} of {total} |{bar}| {percent:.2f}%", end="\n")
    else:
        print(f"\r{task_description} {progress} of {total} |{bar}| {percent:.2f}%", end="\r")
