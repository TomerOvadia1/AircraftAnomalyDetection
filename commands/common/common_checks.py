from data_models.anomaly import Anomaly
from data_models.condition_result import ConditionResult
from typing import List
from data_models.data_row import DataRow


def speed_bounds_check(window_frame: List[DataRow], lower_bound: int, upper_bound: int,
                       command_name: str) -> ConditionResult:
    if not lower_bound < window_frame[-1].airspeed_indicator_indicated_speed_kt < upper_bound:
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          info=f"speed_bounds_check condition is unfulfilled"))
    return ConditionResult.fulfilled_result()


def same_speed_check(window_frame: List[DataRow], command_name: str, window_frame_slice=3) -> ConditionResult:
    if len(window_frame) == 1:
        return ConditionResult.fulfilled_result()
    prev = None
    modified_window_start_point = max(len(window_frame) - window_frame_slice, 0)
    window_frame = window_frame[modified_window_start_point:]
    base_speed = 0
    for data_row in window_frame:
        if not prev:
            prev = data_row
            base_speed = prev.airspeed_indicator_indicated_speed_kt
            continue
        if base_speed != data_row.airspeed_indicator_indicated_speed_kt:
            return ConditionResult.fulfilled_result()
        prev = data_row
    return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                      info=Anomaly.createErrorMsg(
                                                          func_name="__same_speed_check",
                                                          faulty_component="airspeed_indicator_indicated_speed_kt")))


def speed_difference_check(window_frame: List[DataRow], command_name: str, max_diff: int) -> ConditionResult:
    diff = abs(
        window_frame[0].airspeed_indicator_indicated_speed_kt - window_frame[-1].airspeed_indicator_indicated_speed_kt)
    if diff > max_diff:
        msg = f"Misbehavior: Speed difference is bigger than {max_diff} but command is {command_name}"
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          info=Anomaly.createErrorMsg(
                                                              func_name="__speed_difference_check",
                                                              faulty_component=msg)))
    return ConditionResult.fulfilled_result()
