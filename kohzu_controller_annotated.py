import serial
import re


# This dictionary takes the motor as a string "motor number_coordinate_translation/rotation" and returns the right code number
MOTOR_DICT = {
    "g1_x_tra": 1,
    "g1_y_tra": 2,
    "g1_z_tra": 3,
    "g1_x_rot": 4,
    "g1_y_rot": 5,
    "g1_z_rot": 6,
    "g2_x_tra": 7,
    "g2_y_tra": 8,
    "g2_z_tra": 9,
    "g2_x_rot": 10,
    "g2_y_rot": 11,
    "g2_z_rot": 12,
    "g3_x_tra": 13,
    "g3_y_tra": 14,
    "g3_z_tra": 15,
    "g3_x_rot": 16,
    "g3_y_rot": 17,
    "g3_z_rot": 18,
}

# Each motor moves in 'steps', this dictionary converts 'steps; to units of millimeters (for translation) or degrees (for rotation)
MOTOR_UNITS_MM = {
    "g1_x_tra": 0.25e-3,
    "g1_y_tra": 0.05e-3,
    "g1_z_tra": 0.25e-3,
    "g1_x_rot": 0.60e-3,
    "g1_y_rot": 2.00e-3,
    "g1_z_rot": 0.60e-3,
    "g2_x_tra": 0.25e-3,
    "g2_y_tra": 0.05e-3,
    "g2_z_tra": 0.25e-3,
    "g2_x_rot": 0.60e-3,
    "g2_y_rot": 2.00e-3,
    "g2_z_rot": 0.60e-3,
    "g3_x_tra": 0.25e-3,
    "g3_y_tra": 0.05e-3,
    "g3_z_tra": 0.25e-3,
    "g3_x_rot": 0.60e-3,
    "g3_y_rot": 2.00e-3,
    "g3_z_rot": 0.60e-3,
}

# This dictionary returns the full name of each motor, for convinence
MOTOR_NAME_STRS = {
    "g1_x_tra": "G1 X Translation",
    "g1_y_tra": "G1 Y Translation",
    "g1_z_tra": "G1 Z Translation",
    "g1_x_rot": "G1 X Rotation",
    "g1_y_rot": "G1 Y Rotation",
    "g1_z_rot": "G1 Z Rotation",
    "g2_x_tra": "G2 X Translation",
    "g2_y_tra": "G2 Y Translation",
    "g2_z_tra": "G2 Z Translation",
    "g2_x_rot": "G2 X Rotation",
    "g2_y_rot": "G2 Y Rotation",
    "g2_z_rot": "G2 Z Rotation",
    "g3_x_tra": "G3 X Translation",
    "g3_y_tra": "G3 Y Translation",
    "g3_z_tra": "G3 Z Translation",
    "g3_x_rot": "G3 X Rotation",
    "g3_y_rot": "G3 Y Rotation",
    "g3_z_rot": "G3 Z Rotation",
}


class Kohzu_Controller:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        self.axis = tuple(MOTOR_DICT.keys())
        self.axis_numbers = MOTOR_DICT
        self.axis_names = MOTOR_NAME_STRS
        self.axis_units = MOTOR_UNITS_MM

    def add_axis(self, axis_labels: str, axis_numbers: int, axis_names=None) -> None:
        """
        Validates and creates an axis for Kohzu_Controller object.
        """
        if type(axis_numbers) == int and type(axis_labels) == str:
            axis_labels = (axis_labels,)
            axis_numbers = (axis_numbers,)
        elif type(axis_numbers) != type(axis_labels):
            raise ValueError(
                "Axis number and label must be of the same type. Either enter a single axis number and label, or tuples of each."
            )

        for axis_label, axis_number in zip(axis_labels, axis_numbers):
            self.axis += (axis_label,)
            self.axis_numbers[axis_label] = axis_number

    def absolute_position_drive(self, axis: str, speed: int, position: int, output=0):
        """
        Move the motor to specified position in inputted axis at chosen speed.

        Arguments
        axis: name of axis
        speed: motor speed from 1-9
        position: target position of motor in pulse units
        """
        # arguments: (axis, speed, position)
        speed = self._speed_valid(speed)
        self._axis_loaded(axis)

        command = (
            "APS"
            + str(self.axis_numbers[axis])
            + "/"
            + str(speed)
            + "/"
            + str(position)
            + "/"
            + str(output)
        )
        command = command.encode()
        self._write_command(command)

        confirmation = "APS" + str(self.axis_numbers[axis])
        confirmation = confirmation.encode()

        self.ser.timeout = None
        return self.ser.read_until(confirmation, 100)
        # bytestring output. not helpful, useful only because it returns when the process finishes

    def absolute_position_origin(self, axis: str, speed: int, output=0):
        """
        Performs a full recalibration of the motor to the origin point
        using high-precision magnets and lasers along specified axis.

        """

        speed = self._speed_valid(speed)
        self._axis_loaded(axis)

        command = (
            "ORG" + str(self.axis_numbers[axis]) + "/" + str(speed) + "/" + str(output)
        )
        command = command.encode()
        self._write_command(command)

        confirmation = "ORG" + str(self.axis_numbers[axis])
        confirmation = confirmation.encode()

        self.ser.timeout = None
        return self.ser.read_until(confirmation, 100)
        # bytestring output. not helpful, useful only because it returns when the process finishes

    def absolute_position_read(self, axis: str) -> int:
        """
        Returns the motor position in pulse units.
        """

        self._axis_loaded(axis)

        commandstr = "RDP" + str(self.axis_numbers[axis])
        command = commandstr.encode()
        self._write_command(command)

        self.ser.timeout = 0.05
        output = self.ser.read(100)
        output = output.decode("utf-8")

        value = re.search(commandstr + "\t(.*?)\r\n", output)
        if value:
            return value.group(1)
        else:
            return 99999999
        # return value of motor position in the pulse units

    def _axis_loaded(self, axis: str):
        if axis not in self.axis:
            raise ValueError("Axis '%s' not loaded, please add axis to controler ")
        else:
            pass

    def _speed_valid(self, speed: int) -> int:
        """
        Returns a valid speed value: an int from 1-9.
        If speed is not of type int, it will be typecasted to int.
        If speed is less than 1, it will be set to 1 (min value).
        If speed is greater than 9, it will be set to 9 (max value).
        """

        if type(speed) is not int:
            print("Speed setting must be of type int. Casting value to int")
            speed = int(speed)

        if speed < 1:
            print("Speed must be an integer between 1 and 9. Setting to speed to 1.")
            speed = 1
        elif speed > 9:
            print("Speed must be an integer between 1 and 9. Setting to speed to 1.")
            speed = 9

        return speed

    def _write_command(self, command):
        self.ser.write(b"\x02")  # STX
        self.ser.write(command)
        self.ser.write(b"\x0D\x0A")  # CRLF

    def move_grating_out(self, grating_number_tuple=(1, 2, 3)):
        try:
            iter(grating_number_tuple)
        except TypeError:
            grating_number_tuple = (grating_number_tuple,)

        starting_motor_positions = {}

        for grating_number in grating_number_tuple:
            x_tra = self.absolute_position_read(f"g{grating_number:d}_x_tra")
            y_rot = self.absolute_position_read(f"g{grating_number:d}_y_rot")
            starting_motor_positions[f"g{grating_number:d}_x_tra"] = x_tra
            starting_motor_positions[f"g{grating_number:d}_y_rot"] = y_rot

            self.absolute_position_drive(f"g{grating_number:d}_x_tra", 8, -60_000)
            self.absolute_position_drive(
                f"g{grating_number:d}_y_rot", 8, int(90 / MOTOR_UNITS_MM["g1_y_rot"])
            )
        return starting_motor_positions

    def move_grating_in(self, grating_number_tuple=(1, 2, 3), motor_position_dict=None):
        if motor_position_dict is None:
            starting_motor_positions = {}
            for grating_number in grating_number_tuple:
                starting_motor_positions[f"g{grating_number:d}_x_tra"] = 0
                starting_motor_positions[f"g{grating_number:d}_y_rot"] = 0

        for grating_number in grating_number_tuple:
            self.absolute_position_drive(
                f"g{grating_number:d}_x_tra",
                8,
                starting_motor_positions[f"g{grating_number:d}_x_tra"],
            )
            self.absolute_position_drive(
                f"g{grating_number:d}_y_rot",
                8,
                starting_motor_positions[f"g{grating_number:d}_y_rot"],
            )
