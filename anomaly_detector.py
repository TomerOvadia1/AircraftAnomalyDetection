from commands.common.command_factory import CommandFactory
import csv
from data_models.data_row import DataRow,DataRow2
from utils import get_logger


class AnomalyDetector:
    def __init__(self):
        self._log = get_logger(self.__class__.__name__)
        self._factory = CommandFactory()

    def detect_all(self, input_files):
        anomalies_dict = {}
        for file_name in input_files:
            try:
                file_content, anomalies_lst = self.detect_single_file(file_name=file_name)
                anomalies_dict[file_name] = []
                anomalies_dict[file_name].append(file_content)
                anomalies_dict[file_name].append(anomalies_lst)
            except Exception as e:
                self._log.warning(f"Errors found on file {file_name}: {e}")

        return anomalies_dict

    def detect_single_file(self, file_name):
        anomalies = {}
        with open(file_name, "r") as f:
            self._log.info(f"Executing on file {file_name}")
            reader = csv.reader(f, delimiter=",")
            file_content = []
            for i, line in enumerate(reader):
                if i == 0:
                    continue
                try:
                    file_content.append(DataRow(line))
                except Exception as e:
                    file_content.append(DataRow2(line))
            for i, cur_data_row in enumerate(file_content):
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
                        if not anomalies.get(i):
                            anomalies[i] = []
                        anomalies[i].append(condition_result.anomaly)
            if not anomalies:
                self._log.info(f"No anomalies found {file_name}")

            return file_content, anomalies
