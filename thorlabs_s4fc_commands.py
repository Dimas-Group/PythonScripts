import serial
import time
import re

class S4FC_Laser():
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate=baudrate)


    def send_command(self, command='id?'):
        if self.ser.isOpen() != True:
            try:
                self.ser.open()
            except serial.SerialException:
                print('Serial port error, retrying...')
                time.sleep(1)
                self.ser.open()
            
        byteCommand = bytes(command+'\r', 'utf-8')
        self.ser.write(byteCommand)
        output=b''
        time.sleep(1)
        while self.ser.inWaiting() > 0:
            output += self.ser.read(1)
        self.ser.close()
        return output


    def enable_laser(self):
        self.send_command("ENABLE=1")


    def disable_laser(self):
        self.send_command("ENABLE=0")


    def read_laser_output(self):
        response = self.send_command("LD ACTUAL OUTPUT?")
        return self._decode_response_float(response)


    def read_laser_setpoint(self):
        response = self.send_command("LD OUTPUT SETPOINT?")
        return self._decode_response_float(response)


    def read_laser_temperature(self):
        response = self.send_command("LASER TEMP?")
        return self._decode_response_float(response)


    def set_laser_output(self, output_value):
        self.send_command("LD OUTPUT SETPOINT="+str(output_value))


    def _decode_response_float(self, response):
        output = re.search('\r\S+.\S+\r', response.decode("utf-8"))
        return float(output.group()[1:-1])


    def _decode_response_int(self, response):
        output = re.search('\r\S+\r', response.decode("utf-8"))
        return int(output.group()[1:-1])


    def lock_on(self):
        self.send_command("LOCK=1")


    def lock_off(self):
        self.send_command("LOCK=0")


    def lock_toggle(self):
        response = self.send_command("LOCK?")
        lock_state = self._decode_response_int(response)
        self.send_command("LOCK=%d"%((int(lock_state)+1)%2))