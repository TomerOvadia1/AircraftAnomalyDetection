from commands.common.command_factory import CommandFactory
import csv
from data_models.data_row import DataRow
from utils import get_logger
from pprint import pformat


class AnomalyDetector:
    def __init__(self, input_files):
        self._input_files = input_files
        self._log = get_logger(self.__class__.__name__)
        self._factory = CommandFactory()

    def detect(self):
        anomalies = {}
        for file_name in self._input_files:
            anomalies[file_name] = []
            self.single_file_detect(file_name=file_name)

    def single_file_detect(self, file_name):
        anomalies = {}
        with open(file_name, "r") as f:
            self._log.info(f"Executing on file {file_name}")
            reader = csv.reader(f, delimiter=",")
            file_content = []
            for i, line in enumerate(reader):
                if i == 0: continue
                file_content.append(DataRow(line))
            for i, cur_data_row in enumerate(file_content):
                try:
                    # Get window frame
                    cmd = self._factory.get(cur_data_row.command)
                    window_size = cmd.window_size
                    window_frame = []
                    for prev_line in file_content[max(i - window_size + 1, 0):i + 1]:
                        window_frame.append(prev_line)

                    i += 2  # For logging, csv line 1 is headings, and indices start at 1

                    # Check conditions
                    for condition_result in cmd.check_all_conditions(window_frame=window_frame):
                        if not condition_result.is_fulfilled():
                            self._log.info(
                                f"Anomaly line {i}, Command {condition_result.anomaly.name}: {condition_result.anomaly.info}")
                            if not anomalies.get(condition_result.anomaly.info):
                                anomalies[condition_result.anomaly.info] = set()
                            anomalies[condition_result.anomaly.info].add(i)
                except Exception as e:
                    self._log.warning(f"Error on file {file_name} in line {i}: {e}")
            if not anomalies:
                self._log.info(f"No anomalies found {file_name}")
            else:
                self._log.info(f"Anomalies found: \n {pformat(anomalies)}")

            return file_content, anomalies
