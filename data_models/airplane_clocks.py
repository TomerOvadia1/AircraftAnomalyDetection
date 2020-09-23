from enum import Enum


class Clocks(Enum):
    airspeed_indicator_indicated_speed_kt = 1
    altimeter_indicated_altitude_ft = 2
    altimeter_pressure_alt_ft = 3
    attitude_indicator_indicated_pitch_deg = 4
    attitude_indicator_indicated_roll_deg = 5
    attitude_indicator_internal_pitch_deg = 6
    attitude_indicator_internal_roll_deg = 7
    encoder_indicated_altitude_ft = 8
    encoder_pressure_alt_ft = 9
    gps_indicated_altitude_ft = 10
    gps_indicated_ground_speed_kt = 11
    gps_indicated_vertical_speed = 12
    indicated_heading_deg = 13
    magnetic_compass_indicated_heading_deg = 14
    slip_skid_ball_indicated_slip_skid = 15
    turn_indicator_indicated_turn_rate = 16
    vertical_speed_indicator_indicated_speed_fpm = 17
    flight_aileron = 18
    flight_elevator = 19
    flight_rudder = 20
    flight_flaps = 21
    engine_throttle = 22
    engine_rpm = 23
