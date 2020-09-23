from anomaly_detector import AnomalyDetector
import input_data.test_data as test_data
import input_data.cleaned_data.labeld.set1 as set1
import input_data.cleaned_data.labeld.set2 as set2
import input_data.cleaned_data.labeld.set3 as set3
import input_data.cleaned_data.labeld.set4 as set4
import input_data.cleaned_data.labeld.set5 as set5
import os
from results_analyser import ResultsAnalyzer
from predictor import Predictor


def main():
    input_files = [
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog3.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog6.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog9.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog10.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog3.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog6.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog9.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog10.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog3.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog6.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog9.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog10.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog3.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog6.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog9.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog10.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog3.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog6.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog9.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog10.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog12.csv",
    ]
    anomaly_detector = AnomalyDetector()
    anomalies_dict = anomaly_detector.detect_all(input_files=input_files)
    results_analyzer = ResultsAnalyzer()
    results_info_lst = results_analyzer.analyze_all(results=anomalies_dict)
    avg_results = results_analyzer.get_avg_results_info(results_info_lst)
    predictor = Predictor()
    predictor.predict_all(anomalies_dict)
    print('---------------------------------------')
    print(avg_results)


    results_analyzer._test(anomalies_dict)



if __name__ == "__main__":
    main()


'''
    input_files = [
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog3.csv",
        # f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog6.csv",
        # f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog9.csv",
        # f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog10.csv",
        # f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set1.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog3.csv",
        # f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog4.csv",
        # f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog6.csv",
        # f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog9.csv",
        # f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog10.csv",
        # f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set2.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog3.csv",
        # f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog6.csv",
        # f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog9.csv",
        # f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog10.csv",
        # f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set3.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog3.csv",
        # f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog6.csv",
        # f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog9.csv",
        # f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog10.csv",
        # f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set4.__file__))}\\cleaned_flightLog12.csv",

        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog1.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog2.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog3.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog4.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog5.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog6.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog7.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog8.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog9.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog10.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog11.csv",
        f"{os.path.dirname(os.path.abspath(set5.__file__))}\\cleaned_flightLog12.csv",
    ]

'''