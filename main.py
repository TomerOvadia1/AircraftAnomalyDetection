from anomaly_detector import AnomalyDetector

import os
from results_analyser import ResultsAnalyzer
from utils import get_all_csv_files
from predictor import Predictor


def main():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    input_files = get_all_csv_files(cur_dir)
    anomaly_detector = AnomalyDetector()
    anomalies_dict = anomaly_detector.detect_all(input_files=input_files)
    results_analyzer = ResultsAnalyzer()
    results_info_lst = results_analyzer.analyze_all(results=anomalies_dict)
    avg_results = results_analyzer.get_avg_results_info(results_info_lst)
    predictor = Predictor()
    predictor.predict_all(anomalies_dict)
    print(avg_results)


if __name__ == "__main__":
    main()


