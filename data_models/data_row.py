from decimal import *


class DataRow:
    def __init__(self, row):
        self.airspeed_indicator_indicated_speed_kt = Decimal(row[0])
        self.altimeter_indicated_altitude_ft = Decimal(row[1])
        self.altimeter_pressure_alt_ft = Decimal(row[2])
        self.attitude_indicator_indicated_pitch_deg = Decimal(row[3])
        self.attitude_indicator_indicated_roll_deg = Decimal(row[4])
        self.attitude_indicator_internal_pitch_deg = Decimal(row[5])
        self.attitude_indicator_internal_roll_deg = Decimal(row[6])
        self.encoder_indicated_altitude_ft = Decimal(row[7])
        self.encoder_pressure_alt_ft = Decimal(row[8])
        self.gps_indicated_altitude_ft = Decimal(row[9])
        self.gps_indicated_ground_speed_kt = Decimal(row[10])
        self.gps_indicated_vertical_speed = Decimal(row[11])
        self.indicated_heading_deg = Decimal(row[12])
        self.magnetic_compass_indicated_heading_deg = Decimal(row[13])
        self.slip_skid_ball_indicated_slip_skid = Decimal(row[14])
        self.turn_indicator_indicated_turn_rate = Decimal(row[15])
        self.vertical_speed_indicator_indicated_speed_fpm = Decimal(row[16])
        self.flight_aileron = Decimal(row[17])
        self.flight_elevator = Decimal(row[18])
        self.flight_rudder = Decimal(row[19])
        self.flight_flaps = Decimal(row[20])
        self.engine_throttle = Decimal(row[21])
        self.engine_rpm = Decimal(row[22])
        self.command_fault = row[23]
        self.command = row[24].strip().lower()
