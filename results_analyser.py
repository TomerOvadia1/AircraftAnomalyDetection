from typing import List
from data_models.data_row import DataRow
from utils import get_logger


class ResultsAnalyzer:
    def __init__(self, results: dict, data: List[DataRow]):
        self.results = results
        self.data = data
        self._log = get_logger(self.__class__.__name__)

    def analyze(self):
        self._log.info(f"Analyzing results...")

        anomalies_found = self.get_results_anomaly_points()
        anomalies_in_data = self.get_anomalies_in_data()
        data_set = set(i for i in range(len(self.data)))
        non_anomalies_int_data = data_set - anomalies_in_data

        true_positive = anomalies_found & anomalies_in_data
        false_positive = anomalies_found - anomalies_in_data

        true_negative = non_anomalies_int_data - anomalies_found
        false_negative = anomalies_in_data - anomalies_found
        self._log.info(f"Raw data:")
        self._log.info(f"Total anomalies found : {len(anomalies_found)}")
        self._log.info(f"Total anomalies in data : {len(anomalies_in_data)}")

        self._log.info(f"True Positives total : {len(true_positive)}")
        self._log.info(f"False Positives total : {len(false_positive)}")

        self._log.info(f"True Negatives total : {len(true_negative)}")
        self._log.info(f"False Negatives total : {len(false_negative)}")
        self._log.info(f"")

        accuracy = (len(true_positive) + len(true_negative)) / (
                    (len(true_positive) + len(false_negative)) + (len(true_negative) + len(false_positive)))
        recall = len(true_positive) / (len(true_positive) + len(false_negative))
        precision = len(true_positive) / (len(true_positive) + len(false_positive))
        false_positive_rate = len(false_positive)/(len(false_positive) + len(true_negative))

        self._log.info(f"Analyzed results:")
        self._log.info(f"Accuracy : {(accuracy*100):.2f}%")
        self._log.info(f"Recall : {recall*100:.2f}%")
        self._log.info(f"Precision : {precision*100:.2f}%")
        self._log.info(f"False Positive Rate : {false_positive_rate*100:.2f}%")

    def get_results_anomaly_points(self):
        anomalies = set()
        for k, v in self.results.items():
            anomalies.update(v)
        return anomalies

    def get_anomalies_in_data(self):
        data_anomalies = set()
        for i, row in enumerate(self.data):
            if "false" in row.command_fault:
                data_anomalies.add(i)
        return data_anomalies
