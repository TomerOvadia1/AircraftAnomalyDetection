import logging
import os

MAX_VSI_DIFF = 1000


def get_logger(name):
    FORMAT = '%(asctime)-17s %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.NOTSET, format=FORMAT)
    logger = logging.getLogger(name)
    return logger


def get_all_csv_files(dir):
    log = get_logger("GetAllCsvFiles-Helper")
    log.info(f"Reading all csv files for dir {dir}")
    all_files_found = []
    try:
        for subdir, dirs, files in os.walk(dir):
            for file in files:
                # print os.path.join(subdir, file)
                filepath = subdir + os.sep + file
                if filepath.endswith(".csv"):
                    all_files_found.append(filepath)
        log.info(f"Csvs found:")
        for file in all_files_found:
            log.info(f"Found {file}")
        return all_files_found
    except Exception as e:
        log.error(f'Exception: {e}')
        raise e
