from datetime import datetime


def debug(message):
    print(f"\n ::: {datetime.now().strftime('%m/%d/%Y - %H:%M:%S')} ::: DEBUG:", f"{message} \n")
