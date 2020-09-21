from anomaly_detector import AnomalyDetector
import input_data.test_data as test_data
import input_data.cleaned_data.labeld.set2 as cur_set
import os
from results_analyser import ResultsAnalyzer


def main():
    input_files = [
        f"{os.path.dirname(os.path.abspath(cur_set.__file__))}\\cleaned_flightLog3.csv"
    ]
    anomaly_detector = AnomalyDetector(input_files)
    file_content, anomalies = anomaly_detector.single_file_detect(file_name=f"{os.path.dirname(os.path.abspath(cur_set.__file__))}\\cleaned_flightLog3.csv")
    results_analyzer = ResultsAnalyzer(results=anomalies,
                                       data=file_content)
    results_analyzer.analyze()


if __name__ == "__main__":
    main()
