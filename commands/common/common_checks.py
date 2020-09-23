from data_models.anomaly import Anomaly
from data_models.condition_result import ConditionResult
from typing import List
from data_models.data_row import DataRow
from data_models.airplane_clocks import Clocks
from data_models.fault_types import FaultType
from data_models.fault import Fault


def speed_bounds_check(window_frame: List[DataRow], lower_bound: int, upper_bound: int, fault_lst: List[Fault],
                       command_name: str) -> ConditionResult:
    if not lower_bound < window_frame[-1].airspeed_indicator_indicated_speed_kt < upper_bound:
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          description=Anomaly.create_error_msg(
                                                              func_name="speed_bounds_check",
                                                              fault=f"speed_bounds_check condition is unfulfilled"),
                                                          fault_lst=fault_lst))
    return ConditionResult.fulfilled_result()


def attr_is_changing(window_frame: List[DataRow], command_name: str, attr: str, fault_lst: List[Fault],
                     window_frame_slice=3,
                     short_name: str = None) -> ConditionResult:
    short_name = attr if not short_name else short_name
    if len(window_frame) == 1:
        return ConditionResult.fulfilled_result()
    prev = None
    modified_window_start_point = max(len(window_frame) - window_frame_slice, 0)
    window_frame = window_frame[modified_window_start_point:]
    base_speed = 0
    for data_row in window_frame:
        if not prev:
            prev = data_row
            base_speed = getattr(prev, attr)
            continue
        cur_speed = getattr(data_row, attr)
        if base_speed != cur_speed:
            return ConditionResult.fulfilled_result()
        prev = data_row
    return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                      description=Anomaly.create_error_msg(
                                                          func_name=f"attr_{short_name}_is_changing",
                                                          fault=attr),
                                                      fault_lst=fault_lst))


def attr_difference_check(window_frame: List[DataRow], command_name: str, max_diff: int, attr: str,
                          fault_lst: List[Fault],
                          short_name: str = None) -> ConditionResult:
    short_name = attr if not short_name else short_name
    first_row_attr = getattr(window_frame[0], attr)
    last_row_attr = getattr(window_frame[-1], attr)
    diff = abs(first_row_attr - last_row_attr)
    if diff > max_diff:
        msg = f"Misbehavior: {attr} difference is bigger than {max_diff}"
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          description=Anomaly.create_error_msg(
                                                              func_name=f"{short_name}_difference_check",
                                                              fault=msg),
                                                          fault_lst=fault_lst))
    return ConditionResult.fulfilled_result()


def attr_positive_trend_check(window_frame: List[DataRow], attr: str, command_name: str, fault_lst: List[Fault],
                              short_name: str = None, apply_func=None) -> ConditionResult:
    if not apply_func:
        apply_func = lambda x: x
    short_name = attr if not short_name else short_name
    cur_row_attr = apply_func(getattr(window_frame[-1], attr))
    last_row_in_window_attr = apply_func(getattr(window_frame[0], attr))
    if cur_row_attr < last_row_in_window_attr:
        msg = f"{attr} is on a negative trend"
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          description=Anomaly.create_error_msg(
                                                              func_name=f"{short_name}_positive_trend_check",
                                                              fault=msg),
                                                          fault_lst=fault_lst))
    return ConditionResult.fulfilled_result()


def attr_negative_trend_check(window_frame: List[DataRow], attr: str, command_name: str, fault_lst: List[Fault],
                              short_name: str = None, apply_func=None) -> ConditionResult:
    if not apply_func:
        apply_func = lambda x: x
    short_name = attr if not short_name else short_name
    cur_row_attr = apply_func(getattr(window_frame[-1], attr))
    last_row_in_window_attr = getattr(window_frame[0], attr)
    if cur_row_attr > last_row_in_window_attr:
        msg = f"{attr} is on a positive trend"
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          description=Anomaly.create_error_msg(
                                                              func_name=f"{short_name}_negative_trend_check",
                                                              fault=msg),
                                                          fault_lst=fault_lst))
    return ConditionResult.fulfilled_result()


def attr_reached_target_val(window_frame: List[DataRow], attr: str, command_name: str, fault_lst: List[Fault],
                            acc_factor, target_val, short_name: str = None, ) -> ConditionResult:
    short_name = attr if not short_name else short_name
    cur_row_attr = getattr(window_frame[-1], attr)
    if abs(cur_row_attr - target_val) > acc_factor:
        msg = f"{attr} did not reach target value of {target_val} with acc_factor of {acc_factor}"
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          description=Anomaly.create_error_msg(
                                                              func_name=f"{short_name}_reached_target_val",
                                                              fault=msg),
                                                          fault_lst=fault_lst))
    return ConditionResult.fulfilled_result()
