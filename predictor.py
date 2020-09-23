from data_models.anomaly import Anomaly
from data_models.fault import Fault
from data_models.fault_types import FaultType
from data_models.airplane_clocks import Clocks
from enum import Enum
from utils import get_logger
from typing import List


class ConfidenceLevel(Enum):
    low = 1
    medium = 2
    high = 3


class PredictionType(Enum):
    static_fault = 1
    pitot_fault = 1


class Prediction:
    def __init__(self, prediction_type, confidence_level):
        self.prediction_type = prediction_type
        self.confidence_level = confidence_level


class Predictor:
    def __init__(self):
        self._available_predictions = [
            self._predict_static_fault
        ]
        self._log = get_logger(self.__class__.__name__)

    def predict_all(self, file_name_to_findings):
        predictions_dict = {}
        self._log.info(f"Predicting faults for all files")
        for file_name, findings in file_name_to_findings.items():
            index_to_anomalies_dict = findings[1]
            self._log.info(f"Predicting faults for file {file_name}")
            predictions = self.predict_single_file(index_to_anomalies_dict)
            predictions_dict[file_name] = predictions

    def predict_single_file(self, index_to_anomalies_dict):
        predictions = []
        for index, point_anomalies_lst in index_to_anomalies_dict.items():
            for prediction in self._available_predictions:
                prediction_result = prediction(point_anomalies_lst)
                if prediction_result:
                    predictions.append(prediction_result)
                    self._log.info(
                        f"Index {index} : Anomaly results in fault detection: prediction type: {prediction_result.prediction_type}, confidence level: {prediction_result.confidence_level}")
        return predictions

    def _predict_static_fault(self, point_anomalies_lst: List[Anomaly]):
        fault_lst = []

        for single_anomaly in point_anomalies_lst:
            fault_lst += single_anomaly.fault_lst
        alt_is_stuck = False
        vsi_is_stuck = False
        ias_not_in_range = False
        for single_possible_fault in fault_lst:
            alt_is_stuck |= self._alt_is_stuck(single_possible_fault)
            vsi_is_stuck |= self._vsi_is_stuck(single_possible_fault)
            ias_not_in_range |= self._ias_not_in_range(single_possible_fault)
            if alt_is_stuck and vsi_is_stuck and ias_not_in_range:
                break

        confidence_level = None
        if ias_not_in_range:
            confidence_level = ConfidenceLevel.low
        if alt_is_stuck and vsi_is_stuck:
            confidence_level = ConfidenceLevel.medium
            if ias_not_in_range:
                confidence_level = ConfidenceLevel.high
        if confidence_level:
            return Prediction(prediction_type=PredictionType.static_fault,
                              confidence_level=confidence_level)
        return None

    def _alt_is_stuck(self, single_fault: Fault):
        return single_fault.fault_type == FaultType.non_changing and \
               single_fault.clock == Clocks.altimeter_indicated_altitude_ft

    def _vsi_is_stuck(self, single_fault: Fault):
        return single_fault.fault_type == FaultType.non_changing and \
               single_fault.clock == Clocks.vertical_speed_indicator_indicated_speed_fpm

    def _ias_not_in_range(self, single_fault: Fault):
        return single_fault.fault_type == FaultType.exit_bounds and \
               single_fault.clock == Clocks.airspeed_indicator_indicated_speed_kt
