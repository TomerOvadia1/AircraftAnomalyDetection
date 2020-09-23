from enum import Enum


class FaultType(Enum):
    non_changing = 1
    unexpected_negative_trend = 2
    unexpected_positive_trend = 2
    abnormal_diff = 3
    did_not_reach_target_val = 4
    exit_bounds = 5
    non_matching_trends = 6

