from anomaly_detector import AnomalyDetector
import input_data.test_data as test_data
import os
def main():
    input_files = [
        f"{os.path.dirname(os.path.abspath(test_data.__file__))}\\test_speed_fault.csv"
    ]
    anomaly_detector = AnomalyDetector(input_files)
    anomaly_detector.detect()


if __name__ == "__main__":
    main()
