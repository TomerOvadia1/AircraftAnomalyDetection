from anomaly_detector import AnomalyDetector
import input_data.test_data as test_data
import input_data.cleaned_data.labeld.set5 as cur_set
import os


def main():
    input_files = [
        f"{os.path.dirname(os.path.abspath(cur_set.__file__))}\\cleaned_flightLog1.csv"
    ]
    anomaly_detector = AnomalyDetector(input_files)
    anomaly_detector.detect()


if __name__ == "__main__":
    main()
