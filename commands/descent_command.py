from commands.common.command_interface import ICommand
from data_models.condition_result import ConditionResult
from commands.common.common_checks import speed_bounds_check, speed_difference_check, same_speed_check
from typing import List
from data_models.data_row import DataRow
from data_models.anomaly import Anomaly
from data_models.condition_result import ConditionResult


class DescentCommand(ICommand):
    window_size = 10
    command_string = "decent_to_"
    SPEED_MAX_ALLOWED_DIFF = 15
    SPEED_LOWER_BOUND = 55
    SPEED_UPPER_BOUND = 85

    def __init__(self, command):
        super().__init__()
        descent_target_height = command.split(self.command_string)[1]
        descent_target_height = descent_target_height.replace("ft", "")
        self.descent_target_height = int(descent_target_height)
        self.add_condition(self.__speed_bounds_or_speed_inc_check)
        self.add_condition(self.__same_speed_check)
        self.add_condition(self.__speed_difference_check)

    def __speed_bounds_or_speed_inc_check(self, window_frame: List[DataRow]) -> ConditionResult:
        bound_check = speed_bounds_check(lower_bound=DescentCommand.SPEED_LOWER_BOUND,
                                         upper_bound=DescentCommand.SPEED_UPPER_BOUND,
                                         command_name=self.command_string,
                                         window_frame=window_frame)
        # Speed increase status
        speed_dec_check = self.__speed_dec_check(window_frame)

        if not speed_dec_check.is_fulfilled() and not bound_check.is_fulfilled():
            msg = f"Speed is not decreasing on takeoff while plane speed is not following rule -" \
                f" {DescentCommand.SPEED_LOWER_BOUND} < plane_speed < {DescentCommand.SPEED_UPPER_BOUND}"
            return ConditionResult.unfulfilled_result(Anomaly(name=self.command_string,
                                                              info=Anomaly.createErrorMsg(
                                                                  func_name="__speed_bounds_or_speed_inc_check",
                                                                  faulty_component=msg)))
        return ConditionResult.fulfilled_result()

    def __speed_dec_check(self, window_frame: List[DataRow]):
        speed_inc_check = ConditionResult.fulfilled_result()
        if window_frame[0].airspeed_indicator_indicated_speed_kt < window_frame[
            -1].airspeed_indicator_indicated_speed_kt:
            msg = f"Misbehavior: Speed is not decreasing, but command is {self.command_string}"
            speed_inc_check = ConditionResult.unfulfilled_result(Anomaly(name=self.command_string,
                                                                         info=Anomaly.createErrorMsg(
                                                                             func_name="__speed_dec_check",
                                                                             faulty_component=msg)))
        return speed_inc_check

    def __same_speed_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return same_speed_check(window_frame=window_frame,
                                command_name=self.command_string)

    def __speed_difference_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return speed_difference_check(window_frame=window_frame,
                                      command_name=self.command_string,
                                      max_diff=DescentCommand.SPEED_MAX_ALLOWED_DIFF)
