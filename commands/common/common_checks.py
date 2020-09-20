from data_models.anomaly import Anomaly
from data_models.condition_result import ConditionResult


def speed_bounds_check(window_frame, lower_bound, upper_bound, command_name) -> ConditionResult:
    if not lower_bound < window_frame[-1].airspeed_indicator_indicated_speed_kt < upper_bound:
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          info=f"__speed_check condition is unfulfilled"))
    return ConditionResult.fulfilled_result()


def same_speed_check(window_frame, command_name) -> ConditionResult:
    prev = None
    window_frame = window_frame[len(window_frame) - 2:]
    for data_row in window_frame:
        if not prev:
            prev = data_row
            continue
        if prev.airspeed_indicator_indicated_speed_kt == data_row.airspeed_indicator_indicated_speed_kt:
            return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                              info=Anomaly.createErrorMsg(
                                                                  func_name="__same_speed_check",
                                                                  faulty_component="airspeed_indicator_indicated_speed_kt")))
        prev = data_row
    return ConditionResult.fulfilled_result()


def speed_difference_check(window_frame, command_name, max_diff) -> ConditionResult:
    if abs(window_frame[0].airspeed_indicator_indicated_speed_kt - window_frame[-1].airspeed_indicator_indicated_speed_kt) > max_diff:
        return ConditionResult.unfulfilled_result(Anomaly(name=command_name,
                                                          info=Anomaly.createErrorMsg(
                                                              func_name="__speed_difference_check",
                                                              faulty_component=f"Misbehavior: Speed difference is bigger than {max_diff} but command is {command_name}")))
    return ConditionResult.fulfilled_result()

