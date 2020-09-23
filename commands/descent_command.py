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


class DescentCommand(ICommand):
    window_size = 10
    command_string = "decent_to_"
    SPEED_MAX_ALLOWED_DIFF = 15
    SPEED_LOWER_BOUND = 55
    SPEED_UPPER_BOUND = 85
    VSI_EPSILON_ACC_FACTOR = 200
    VSI_TARGET_VAL = -700

    def __init__(self, command):
        super().__init__()
        descent_target_height = command.split(self.command_string)[1]
        descent_target_height = descent_target_height.replace("ft", "")
        self.descent_target_height = int(descent_target_height)
        self.add_all_conditions([
            self.__speed_bounds_or_speed_dec_check,
            self.__speed_is_changing,
            self.__speed_difference_check,
            self.__vsi_difference_check,
            self.__vsi_is_changing,
            self.__vsi_negative_alt_neg_trend_check,
            self.__alt_is_changing,
            self.__magnetic_is_changing,
            self.__heading_is_changing,
            self.__flight_elevator_is_changing

        ])

    def __speed_bounds_or_speed_dec_check(self, window_frame: List[DataRow]) -> ConditionResult:
        bound_check = common_checks.speed_bounds_check(lower_bound=DescentCommand.SPEED_LOWER_BOUND,
                                                       upper_bound=DescentCommand.SPEED_UPPER_BOUND,
                                                       command_name=self.command_string,
                                                       window_frame=window_frame,
                                                       fault_lst=[
                                                           Fault(
                                                               clock=Clocks.airspeed_indicator_indicated_speed_kt,
                                                               fault_type=FaultType.exit_bounds)
                                                       ]
                                                       )
        # Speed increase status
        speed_dec_check = self.__speed_dec_check(window_frame)

        if not speed_dec_check.is_fulfilled() and not bound_check.is_fulfilled():
            msg = f"Speed is not decreasing on takeoff while plane speed is not following rule -" \
                f" {DescentCommand.SPEED_LOWER_BOUND} < plane_speed < {DescentCommand.SPEED_UPPER_BOUND}"
            return ConditionResult.unfulfilled_result(Anomaly(name=self.command_string,
                                                              description=Anomaly.create_error_msg(
                                                                  func_name="__speed_bounds_or_speed_dec_check",
                                                                  fault=msg),
                                                              fault_lst=[
                                                                  Fault(
                                                                      clock=Clocks.airspeed_indicator_indicated_speed_kt,
                                                                      fault_type=FaultType.exit_bounds),
                                                                  Fault(
                                                                      clock=Clocks.airspeed_indicator_indicated_speed_kt,
                                                                      fault_type=FaultType.unexpected_positive_trend)
                                                              ]
                                                              ))
        return ConditionResult.fulfilled_result()

    def __speed_dec_check(self, window_frame: List[DataRow]):
        return common_checks.attr_negative_trend_check(window_frame=window_frame,
                                                       attr='airspeed_indicator_indicated_speed_kt',
                                                       command_name=self.command_string,
                                                       short_name='IAS',
                                                       fault_lst=[
                                                           Fault(
                                                               clock=Clocks.airspeed_indicator_indicated_speed_kt,
                                                               fault_type=FaultType.unexpected_positive_trend)
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
                                                   max_diff=DescentCommand.SPEED_MAX_ALLOWED_DIFF,
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

    def __vsi_negative_alt_neg_trend_check(self, window_frame: List[DataRow]) -> ConditionResult:
        if window_frame[0].vertical_speed_indicator_indicated_speed_fpm < 0:
            return common_checks.attr_negative_trend_check(window_frame=window_frame,
                                                           attr='altimeter_indicated_altitude_ft',
                                                           command_name=self.command_string,
                                                           short_name='ALT',
                                                           fault_lst=[
                                                               Fault(
                                                                   clock=Clocks.altimeter_indicated_altitude_ft,
                                                                   fault_type=FaultType.unexpected_positive_trend)
                                                           ]
                                                           )
        return ConditionResult.fulfilled_result()

    def __desc_vsi_negative_trend_check(self, window_frame: List[DataRow]) -> ConditionResult:
        negative_trend_result = common_checks.attr_negative_trend_check(window_frame=window_frame,
                                                                        attr='vertical_speed_indicator_indicated_speed_fpm',
                                                                        command_name=self.command_string,
                                                                        short_name='VSI',
                                                                        fault_lst=[
                                                                            Fault(
                                                                                clock=Clocks.vertical_speed_indicator_indicated_speed_fpm,
                                                                                fault_type=FaultType.unexpected_positive_trend)
                                                                        ]
                                                                        )
        if negative_trend_result.is_fulfilled():
            return negative_trend_result
        return common_checks.attr_reached_target_val(window_frame=window_frame,
                                                     attr='vertical_speed_indicator_indicated_speed_fpm',
                                                     command_name=self.command_string,
                                                     short_name='VSI',
                                                     acc_factor=DescentCommand.VSI_EPSILON_ACC_FACTOR,
                                                     target_val=DescentCommand.VSI_TARGET_VAL,
                                                     fault_lst=[
                                                         Fault(
                                                             clock=Clocks.vertical_speed_indicator_indicated_speed_fpm,
                                                             fault_type=FaultType.did_not_reach_target_val)
                                                     ]
                                                     )

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
