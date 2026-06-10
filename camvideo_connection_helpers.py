# Before importing these functions, the calling file must run the CLR load
# sequence with AE.SWP800000.Library.LoadAssetLibraries()

# Import required modules
from AE.SWP800018.Interfaces import *
from AE.SWP800018.Processing import *
from AE.SWP800018.Cameras import *
import AE.SWP800008 as SERIAL

# Creates a new camera
# Returns None on fail
def create_camera(name = None):
	if (name == None):
		# Get selection
		selection = None
		while not name:
			# Load current cameras
			cameras = CameraBase.FindCameras()
			camera_cnt = cameras.Length

			# Print selections
			for x in range(camera_cnt):
				print(str(x) + ": " + cameras[x])
			
			# Get selection
			selection = input("Camera: ")
			if not selection:
				print("No Selection!\n")
				continue

			# Parse selection
			if any(c.isalpha() for c in selection):
				name = selection
			else:
				selection = int(selection)
				if (camera_cnt < selection):
					print("Bad Selection\n")
					continue
				name = cameras[selection]
		print("")

	# Create the Camera Device
	return CameraBase.CreateCamera(name);

# Creates a new serial or device controller
# Returns None on fail
def create_controller(device_type = None, name = None, BaudRate = 115200):
	# Check if selection provided (prompt if not)
	if (name == None):
		# Get available
		devices = SERIAL.Controller.Ports
		device_cnt = devices.Length

		# Get selection
		while (name == None):
			for x in range(device_cnt):
				print(str(x) + ": " + devices[x])
			
			# Get selection
			selection = input("Control: ")
			if not selection:
				print("No Selection!\n")
				continue

			# Parse selection
			if "COM" in selection:
				name = selection
			elif any(c.isalpha() for c in selection):
				print("Invalid Input!")
				continue
			else:
				selection = int(selection)
				if (device_cnt <= selection):
					print("Bad Selection!\n")
					continue
				name = devices[selection]
		print("")

	# Create the Serial control instance
	control_info = SERIAL.PortInfo(name, BaudRate);
	control_serial = SERIAL.Controller(control_info);

	# Check control valid
	if not (control_serial.Open() and control_serial.IsValid):
		print("Controller is Invalid! Error: " + control_serial.LastError)
		control_serial.Close()
		return None

	# Create control device or return serial device
	if (device_type != None):
		return device_type(control_serial)
	else:
		return control_serial
