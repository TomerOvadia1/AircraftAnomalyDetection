from typing import List
from data_models.data_row import DataRow
from utils import get_logger


class ResultsInfo:
    def __init__(self, accuracy, recall, precision, false_positive_rate):
        self.accuracy = accuracy
        self.recall = recall
        self.precision = precision
        self.false_positive_rate = false_positive_rate

    def __str__(self):
        return f"Accuracy : {(self.accuracy * 100):.2f}%\n" \
            f"Recall : {self.recall * 100:.2f}% -> low = not enough anomalies\n" \
            f"Precision : {self.precision * 100:.2f}% -> how much detected_anomalies are really anomalies\n" \
            f"False Positive Rate : {self.false_positive_rate * 100:.2f}%"


class ResultsAnalyzer:
    def __init__(self):
        self._log = get_logger(self.__class__.__name__)

    def analyze_all(self, results: dict):
        results_info_lst = []
        for file_name, findings in results.items():
            file_content = findings[0]
            anomalies = findings[1]
            self._log.info(f"Analyzing {file_name}")
            results_info_lst.append(self.analyze_single_file(file_content, anomalies))
        return results_info_lst

    def analyze_single_file(self, file_content, anomalies):
        self._log.info(f"Analyzing results...")

        anomalies_found = self.get_results_anomaly_points(anomalies)
        anomalies_in_data = self.get_anomalies_in_data(file_content)
        data_set = set(i for i in range(len(file_content)))
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
        recall = len(true_positive) / (len(true_positive) + len(false_negative)) if (len(true_positive) + len(false_negative))!=0 else 0
        precision = len(true_positive) / (len(true_positive) + len(false_positive)) if (len(true_positive) + len(false_positive))!=0 else 0
        false_positive_rate = len(false_positive) / (len(false_positive) + len(true_negative)) if (len(false_positive) + len(true_negative))!=0 else 0

        self._log.info(f"Analyzed results:")
        self._log.info(f"Accuracy : {(accuracy * 100):.2f}%")
        self._log.info(f"Recall : {recall * 100:.2f}% -> low = not enough anomalies")
        self._log.info(f"Precision : {precision * 100:.2f}% -> how much detected_anomalies are really anomalies")
        self._log.info(f"False Positive Rate : {false_positive_rate * 100:.2f}%")
        return ResultsInfo(
            accuracy=accuracy,
            recall=recall,
            precision=precision,
            false_positive_rate=false_positive_rate
        )

    def get_results_anomaly_points(self, anomalies):
        _anomalies = set()
        for k, v in anomalies.items():
            _anomalies.add(k)
        return _anomalies

    def get_anomalies_in_data(self, file_content):
        data_anomalies = set()
        for i, row in enumerate(file_content):
            if "false" in row.command_fault:
                data_anomalies.add(i)
        return data_anomalies

    @staticmethod
    def get_avg_results_info(results_info_lst: List[ResultsInfo]):
        avg_accuracy = 0
        avg_recall = 0
        avg_precision = 0
        avg_false_positive_rate = 0
        for result_info in results_info_lst:
            avg_accuracy += result_info.accuracy
            avg_recall += result_info.recall
            avg_precision += result_info.precision
            avg_false_positive_rate += result_info.false_positive_rate
        avg_accuracy /= len(results_info_lst)
        avg_recall /= len(results_info_lst)
        avg_precision /= len(results_info_lst)
        avg_false_positive_rate /= len(results_info_lst)
        return ResultsInfo(
            accuracy=avg_accuracy,
            recall=avg_recall,
            precision=avg_precision,
            false_positive_rate=avg_false_positive_rate
        )

    def _test(self, results):
        total_data = 0
        total_anomalies = 0

        for file_name, findings in results.items():
            file_content = findings[0]
            total_data+= len(file_content)
            anomalies_in_data = self.get_anomalies_in_data(file_content)
            total_anomalies += len(anomalies_in_data)
        print("TOTALS")
        print(total_data)
        print(total_anomalies)
