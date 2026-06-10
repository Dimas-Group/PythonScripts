import serial
import re

class Kohzu_Controller():
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        self.axis = ()
        self.axis_numbers = {}
        self.axis_names = {}
        self.axis_units = {}


    def add_axis(self, axis_labels, axis_numbers, axis_names=None):
        if type(axis_numbers) == int and type(axis_labels) == str:
            axis_labels = (axis_labels, )
            axis_numbers = (axis_numbers, )
        elif type(axis_numbers) != type(axis_labels):
            raise ValueError("Axis number and label must be of the same type. Either enter a single axis number and label, or tuples of each.")
        
        for (axis_label, axis_number) in zip(axis_labels, axis_numbers):
            self.axis += (axis_label, )
            self.axis_numbers[axis_label] = axis_number


    def absolute_position_drive(self, axis, speed, position, output=0): 
        #arguments: (axis, speed, position)
        
        speed = self._speed_valid(speed)
        self._axis_loaded(axis)

        command = 'APS' + str(self.axis_numbers[axis]) + '/' + str(speed) + '/' + str(position) + '/' + str(output)
        command = command.encode()
        self._write_command(command)

        confirmation = 'APS' + str(self.axis_numbers[axis])
        confirmation = confirmation.encode()

        self.ser.timeout = None
        return self.ser.read_until(confirmation,100)
        # bytestring output. not helpful, useful only because it returns when the process finishes
        

    def absolute_position_origin(self, axis, speed, output=0): 
        #arguments: (axis, speed, position)
        
        speed = self._speed_valid(speed)
        self._axis_loaded(axis)

        command = 'ORG' + str(self.axis_numbers[axis]) + '/' + str(speed)  + '/' + str(output)
        command = command.encode()
        self._write_command(command)

        confirmation = 'ORG' + str(self.axis_numbers[axis])
        confirmation = confirmation.encode()

        self.ser.timeout = None
        return self.ser.read_until(confirmation,100)
        # bytestring output. not helpful, useful only because it returns when the process finishes


    def absolute_position_read(self, axis): 
        #arguments: (axis)
        
        self._axis_loaded(axis)

        commandstr = 'RDP' + str(self.axis_numbers[axis])
        command = commandstr.encode() 
        self._write_command(command)

        self.ser.timeout = 0.05
        output = self.ser.read(100)
        output = output.decode("utf-8") 

        value = re.search(commandstr+'\t(.*?)\r\n', output)
        if value: 
            return(value.group(1))
        else: 
            return(99999999)
        # return value of motor position in the pulse units


    def _axis_loaded(self, axis):
        if axis not in self.axis:
            raise ValueError("Axis '%s' not loaded, please add axis to controler ")
        else:
            pass

        
    def _speed_valid(self, speed):
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
        self.ser.write(b'\x02') #STX
        self.ser.write(command)
        self.ser.write(b'\x0D\x0A') #CRLF

