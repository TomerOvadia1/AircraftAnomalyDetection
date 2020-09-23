from commands.common.command_interface import ICommand
from data_models.condition_result import ConditionResult
from typing import List
from data_models.data_row import DataRow
from data_models.anomaly import Anomaly
from data_models.condition_result import ConditionResult
from utils import MAX_VSI_DIFF
import commands.common.common_checks as common_checks
from data_models.airplane_clocks import Clocks
from data_models.fault import Fault
from data_models.fault_types import FaultType


class TurnCommand(ICommand):
    window_size = 10
    command_string = "turn_"
    SPEED_MAX_ALLOWED_DIFF = 10
    SPEED_LOWER_BOUND = 45
    SPEED_UPPER_BOUND = 110

    def __init__(self, command):
        super().__init__()
        turn_degree = command.split(self.command_string)[1]
        mult_factor = 1 if turn_degree[0] == "+" else -1
        turn_degree = int(turn_degree) * mult_factor
        self.turn_degree = turn_degree
        self.add_all_conditions([
            self.__speed_bounds_check,
            self.__speed_is_changing,
            self.__speed_difference_check,
            self.__vsi_difference_check,
            self.__vsi_is_changing,
            self.__vsi_positive_alt_pos_trend_check,
            self.__alt_is_changing,
            self.__magnetic_is_changing,
            # self.__same_trend_check_magnetic_and_heading,
            self.__heading_is_changing,
            self.__flight_elevator_is_changing
        ])

    def __speed_bounds_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.speed_bounds_check(lower_bound=TurnCommand.SPEED_LOWER_BOUND,
                                                upper_bound=TurnCommand.SPEED_UPPER_BOUND,
                                                command_name=self.command_string,
                                                window_frame=window_frame,
                                                fault_lst=[
                                                    Fault(
                                                        clock=Clocks.airspeed_indicator_indicated_speed_kt,
                                                        fault_type=FaultType.exit_bounds)
                                                ]
                                                )

    def __speed_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="airspeed_indicator_indicated_speed_kt",
                                              short_name='IAS',
                                              fault_lst=[
                                                  Fault(clock=Clocks.airspeed_indicator_indicated_speed_kt,
                                                        fault_type=FaultType.non_changing)
                                              ]
                                              )

    def __speed_difference_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_difference_check(window_frame=window_frame,
                                                   command_name=self.command_string,
                                                   max_diff=TurnCommand.SPEED_MAX_ALLOWED_DIFF,
                                                   attr='airspeed_indicator_indicated_speed_kt',
                                                   short_name='IAS',
                                                   fault_lst=[
                                                       Fault(clock=Clocks.airspeed_indicator_indicated_speed_kt,
                                                             fault_type=FaultType.abnormal_diff)
                                                   ]
                                                   )

    def __vsi_difference_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_difference_check(window_frame=window_frame,
                                                   command_name=self.command_string,
                                                   max_diff=MAX_VSI_DIFF,
                                                   attr='vertical_speed_indicator_indicated_speed_fpm',
                                                   short_name='VSI',
                                                   fault_lst=[
                                                       Fault(clock=Clocks.vertical_speed_indicator_indicated_speed_fpm,
                                                             fault_type=FaultType.abnormal_diff)
                                                   ]
                                                   )

    def __vsi_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="vertical_speed_indicator_indicated_speed_fpm",
                                              short_name="VSI",
                                              fault_lst=[
                                                  Fault(clock=Clocks.vertical_speed_indicator_indicated_speed_fpm,
                                                        fault_type=FaultType.non_changing)
                                              ]
                                              )

    def __vsi_positive_alt_pos_trend_check(self, window_frame: List[DataRow]) -> ConditionResult:
        if window_frame[0].vertical_speed_indicator_indicated_speed_fpm > 0:
            return common_checks.attr_positive_trend_check(window_frame=window_frame,
                                                           attr='altimeter_indicated_altitude_ft',
                                                           command_name=self.command_string,
                                                           short_name='ALT',
                                                           fault_lst=[
                                                               Fault(
                                                                   clock=Clocks.altimeter_indicated_altitude_ft,
                                                                   fault_type=FaultType.unexpected_negative_trend)
                                                           ]
                                                           )
        return ConditionResult.fulfilled_result()

    def __alt_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="altimeter_indicated_altitude_ft",
                                              short_name='ALT',
                                              fault_lst=[
                                                  Fault(
                                                      clock=Clocks.altimeter_indicated_altitude_ft,
                                                      fault_type=FaultType.non_changing)
                                              ]
                                              )

    def __magnetic_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="magnetic_compass_indicated_heading_deg",
                                              short_name='Magnetic-Compass',
                                              fault_lst=[
                                                  Fault(
                                                      clock=Clocks.magnetic_compass_indicated_heading_deg,
                                                      fault_type=FaultType.non_changing)
                                              ]
                                              )

    # def __same_trend_check_magnetic_and_heading(self, window_frame: List[DataRow]) -> ConditionResult:
    #     def deg_modulo(x):
    #         return x % 360
    #
    #     magnetic_positive_trend_check = common_checks.attr_positive_trend_check(window_frame=window_frame,
    #                                                                             attr='magnetic_compass_indicated_heading_deg',
    #                                                                             command_name=self.command_string,
    #                                                                             short_name='MGNT',
    #                                                                             apply_func=deg_modulo)
    #
    #     heading_positive_trend_check = common_checks.attr_positive_trend_check(window_frame=window_frame,
    #                                                                            attr='indicated_heading_deg',
    #                                                                            command_name=self.command_string,
    #                                                                            short_name='HDG',
    #                                                                            apply_func=deg_modulo)
    #
    #     if heading_positive_trend_check.is_fulfilled() or magnetic_positive_trend_check.is_fulfilled():
    #         if not (heading_positive_trend_check.is_fulfilled() and magnetic_positive_trend_check.is_fulfilled()):
    #             msg = 'Heading or Magnetic is on positive trend, but not both'
    #             return ConditionResult.unfulfilled_result(Anomaly(name=self.command_string,
    #                                                               description=Anomaly.create_error_msg(
    #                                                                   func_name=f"__same_trend_check_magnetic_and_heading",
    #                                                                   fault=msg)))
    #     return ConditionResult.fulfilled_result()

    def __heading_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="indicated_heading_deg",
                                              short_name='HDG',
                                              fault_lst=[
                                                  Fault(
                                                      clock=Clocks.indicated_heading_deg,
                                                      fault_type=FaultType.non_changing)
                                              ]
                                              )

    def __flight_elevator_is_changing(self, window_frame: List[DataRow]) -> ConditionResult:
        return common_checks.attr_is_changing(window_frame=window_frame,
                                              command_name=self.command_string,
                                              attr="flight_elevator",
                                              short_name='ELV',
                                              fault_lst=[
                                                  Fault(
                                                      clock=Clocks.flight_elevator,
                                                      fault_type=FaultType.non_changing)
                                              ]
                                              )
