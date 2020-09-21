from commands.common.command_interface import ICommand
from data_models.condition_result import ConditionResult
from typing import List
from data_models.data_row import DataRow
from data_models.anomaly import Anomaly
from data_models.condition_result import ConditionResult
from utils import MAX_VSI_DIFF
import commands.common.common_checks as common_checks


class TakeoffCommand(ICommand):
    command_string = "takeoff"
    window_size = 20
    SPEED_MAX_ALLOWED_DIFF = 25
    SPEED_LOWER_BOUND = 45
    SPEED_UPPER_BOUND = 85
    VSI_EPSILON_ACC_FACTOR = 50
    TAKEOFF_TARGET_ALT = 1000

    def __init__(self):
        super().__init__()
        self._takeoff_target_alt = TakeoffCommand.TAKEOFF_TARGET_ALT
        self.add_all_conditions([
            self.__speed_bounds_or_speed_inc_check,
            self.__speed_is_changing,
            self.__speed_difference_check,
            self.__vsi_difference_check,
            self.__vsi_is_changing,
            self.__vsi_positive_alt_pos_trend_check,
            self.__alt_is_changing
        ])

    def __speed_bounds_or_speed_inc_check(self, window_frame: List[DataRow]) -> ConditionResult:
        bound_check = common_checks.speed_bounds_check(lower_bound=TakeoffCommand.SPEED_LOWER_BOUND,
                                                       upper_bound=TakeoffCommand.SPEED_UPPER_BOUND,
                                                       command_name=self.command_string,
                                                       window_frame=window_frame)
        # Speed increase status
        speed_inc_check = self.__speed_inc_check(window_frame)

        if not speed_inc_check.is_fulfilled() and not bound_check.is_fulfilled():
            msg = f"Speed is not increasing on takeoff while plane speed is not following rule -" \
                f" {TakeoffCommand.SPEED_LOWER_BOUND} < plane_speed < {TakeoffCommand.SPEED_UPPER_BOUND}"
            return ConditionResult.unfulfilled_result(Anomaly(name=self.command_string,
                                                              info=Anomaly.create_error_msg(
                                                                  func_name="__speed_bounds_or_speed_inc_check",
                                                                  fault=msg)))
        return ConditionResult.fulfilled_result()

    def __speed_inc_check(self, window_frame: List[DataRow]):
        speed_inc_check = ConditionResult.fulfilled_result()
        if window_frame[0].airspeed_indicator_indicated_speed_kt > window_frame[
            -1].airspeed_indicator_indicated_speed_kt:
            msg = f"Misbehavior: Speed is not increasing, but command is {self.command_string}"
            speed_inc_check = ConditionResult.unfulfilled_result(Anomaly(name=self.command_string,
                                                                         info=Anomaly.create_error_msg(
                                                                             func_name="__speed_inc_check",
                                                                             fault=msg)))
        return speed_inc_check

    def __speed_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="airspeed_indicator_indicated_speed_kt",
                                              short_name='IAS')

    def __speed_difference_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_difference_check(window_frame=window_frame,
                                                   command_name=self.command_string,
                                                   max_diff=TakeoffCommand.SPEED_MAX_ALLOWED_DIFF,
                                                   attr='airspeed_indicator_indicated_speed_kt',
                                                   short_name='IAS')

    def __vsi_difference_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_difference_check(window_frame=window_frame,
                                                   command_name=self.command_string,
                                                   max_diff=MAX_VSI_DIFF,
                                                   attr='vertical_speed_indicator_indicated_speed_fpm',
                                                   short_name='VSI')

    def __vsi_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="vertical_speed_indicator_indicated_speed_fpm",
                                              short_name="VSI")

    def __vsi_positive_alt_pos_trend_check(self, window_frame: List[DataRow]) -> ConditionResult:
        if window_frame[0].vertical_speed_indicator_indicated_speed_fpm > 0:
            return common_checks.attr_positive_trend_check(window_frame=window_frame,
                                                           attr='altimeter_indicated_altitude_ft',
                                                           command_name=self.command_string,
                                                           short_name='ALT')
        return ConditionResult.fulfilled_result()

    def __alt_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="altimeter_indicated_altitude_ft",
                                              short_name='ALT')

    # def __takeoff_vsi_negative_trend_check(self, window_frame: List[DataRow]) -> ConditionResult:
    #     negative_trend_result = common_checks.attr_positive_trend_check(window_frame=window_frame,
    #                                                                     attr='vertical_speed_indicator_indicated_speed_fpm',
    #                                                                     command_name=self.command_string,
    #                                                                     short_name='VSI')
    #     if negative_trend_result.is_fulfilled():
    #         return negative_trend_result
    #     return common_checks.attr_reached_target_val(window_frame=window_frame,
    #                                                  attr='vertical_speed_indicator_indicated_speed_fpm',
    #                                                  command_name=self.command_string,
    #                                                  short_name='VSI',
    #                                                  acc_factor=TakeoffCommand.VSI_EPSILON_ACC_FACTOR,
    #                                                  target_val=self._takeoff_target_alt)


