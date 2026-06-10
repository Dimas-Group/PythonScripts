import sys
import os
import clr
import time
import numpy as np

# Check python 32-bit or 64-bit
if sys.maxsize <= 2**32:
    print("Python x64 bit required")
    exit(1)

# Save curret path (used for calling files)
cwd_script = os.getcwd()
#print("cwd_script:", cwd_script)

# Setup absolute path
dll_dir_absolute_path = cwd_script + "/CamVideo-v0.25.0-PhoenixCamera-vX.XX.X/lib/"

#dll_dir_absolute_path = cwd_script + "/../CamVideo-v0.25.0-PhoenixCamera-vX.XX.X/lib/"

# Add references to Base DLL
# Must be absolute path otherwise get NTFS file blocked error
#abs_path = r"C:\Users\Dima's group\Documents\Python Scripts\CamVideo-v0.25.0-PhoenixCamera-vX.XX.X\lib\netstandard2.0\AE.SWP800000.dll"
clr.AddReference(dll_dir_absolute_path + "netstandard2.0/AE.SWP800000.dll")
import AE.SWP800000

# Use library asset loader to load assemblies
AE.SWP800000.Library.LoadAssetLibraries()

# Import required modules
from AE.SWP800018.Interfaces import *
from AE.SWP800018.Processing import *
import AE.SWP800022 as DEVICE
from System import UInt16
from camvideo_connection_helpers import create_camera, create_controller


# class AttolloCamera:
#     def __init__(self, cam_str="[USB-0] FX3", cont_str="COM19"):
#         # Find and create a Camera Device
#         self.camera = create_camera(cam_str)
#         print("Is camera open?:", self.camera.Open())

#         if self.camera == None:
#             print("Failed to connect to camera")
#             exit(1)

#         if not self.camera.Open():
#             print("Failed to open camera")
#             exit(1)

#         # Find and create a Control Device
#         self.control = create_controller(DEVICE.Controller, cont_str)

#         if self.control == None:
#             print("Control Connection Failed")
#             self.camera.Close()
#             exit(1)

#         # Set camera to live
#         self.camera.IsLive = True

#         # Wait for camera to have frame ready
#         while not self.camera.IsReady:
#             print("No Image... Sleeping...")
#             time.sleep(0.5)

#         self.image = None

#     def set_gain(self, gain_val, offset_val=0):
#         self.control.SetAGCMode(0, 1)  # Set Auto-Gain mode to Manual
#         self.control.SetAGCGain(0, gain_val)
#         self.control.SetAGCOffset(0, offset_val)

#     def set_exposure(self, exposure_val, exposure_time=None):
#         self.control.SetAECMode(0, 0)
#         if exposure_time is None:
#             self.control.SetIntegrationTimeRegister(0, exposure_val)
#             print("exposure_time is None")
#         else:
#             self.control.SetIntegrationTimeMS(0, exposure_time)

#     def set_image_dtype(self, N_bits=8):
#         if N_bits == 8:
#             dtype = DEVICE.Controller.COLOR_MODE.MONO8
#         elif N_bits == 10:
#             dtype = DEVICE.Controller.COLOR_MODE.MONO10
#         elif N_bits == 12:
#             dtype = DEVICE.Controller.COLOR_MODE.MONO12
#         elif N_bits == 14:
#             dtype = DEVICE.Controller.COLOR_MODE.MONO14
#         elif N_bits == 16:
#             dtype = DEVICE.Controller.COLOR_MODE.MONO16
#         else:
#             print("Number of bits not in allowed values, defaulting to 16-bit.")
#             dtype = DEVICE.Controller.COLOR_MODE.MONO16
#         self.control.SetColorMode(0, dtype)

#     def _save_image(self, filename="tmp", fileformat="txt"):
#         if fileformat == "txt":
#             AE.SWP800018.Processing.Codecs.TEXT.Save(self.camera.Image, filename+".txt")
#         elif fileformat == "png":
#             self.camera.Image.SaveImage(filename+".png")
#         else:
#             print(f"File format {fileformat} not recognized. Defaulting to TXT.")
#             self._save_image(filename=filename, fileformat="txt")
            
#     def _capture_image(self):
#         self._save_image(filename="tmp", fileformat="txt")
#         self.image = np.loadtxt("tmp.txt")
#         os.remove("tmp.txt")

#     def return_image(self):
#         self._capture_image()
#         return self.image
    
#     def save_image(self, filename, fileformat="png"):
#         self._save_image(filename, fileformat)

#     def return_image_mean(self):
#         self._capture_image()
#         return np.mean(self.image)

#     def return_image_statistics(self):
#         self._capture_image()
#         return (np.mean(self.image), np.std(self.image))
    
#     def return_temp(self):
#         self.control.TEMPERATURE_UNITS.CELSIUS

#         part_labels = ["DETECTOR", "FPGA_JUNCTION", "DETECTOR_BOARD", "PROCESSOR_BOARD"]

#         temp_list = [self.control.GetTemperature(i) for i in range(len(part_labels))]

#         # for i in range(len(part_labels)):

#         #     print(self.control.GetTemperature(i))


#         return temp_list

#     def close(self):
#         self.camera.Close()
#         self.control.ControlInterface.Close()


class AttolloCamera:
    def __init__(self, cam_str="[USB-0] FX3", cont_str="COM19"):
        # Find and create a Camera Device
        self.camera = create_camera(cam_str)
        print(self.camera.Open())

        if self.camera == None:
            print("Failed to connect to camera")
            exit(1)

        if not self.camera.Open():
            print("Failed to open camera")
            exit(1)

        # Find and create a Control Device
        self.control = create_controller(DEVICE.Controller, cont_str)

        if self.control == None:
            print("Control Connection Failed")
            self.camera.Close()
            exit(1)

        try:
            # You had this commented out later in your code; it is likely required here:
            self.control.SetInputMode(0, DEVICE.Controller.INPUT_MODE.NORMAL)   
            
            # Ensure the global frame enable is on
            self.control.SetFrameModeGlobal(DEVICE.Controller.FRAME_MODE_GLOBAL_FLAGS.FRAME_EN)
        except Exception as e:
            print(f"Warning: Could not set input mode: {e}")
        
        # Set camera to live
        self.camera.IsLive = True

        # Wait for camera to have frame ready
        while not self.camera.IsReady:
            print("No Image... Sleeping...")
            time.sleep(0.5)

        self.image = None

    def set_gain(self, gain_val, offset_val=0):
        self.control.SetAGCMode(0, 1)  # Set Auto-Gain mode to Manual
        self.control.SetAGCGain(0, gain_val)
        self.control.SetAGCOffset(0, offset_val)

    def set_exposure(self, exposure_val, exposure_time=None):
        self.control.SetAECMode(0, 0)

        if exposure_time is None:
            self.control.SetIntegrationTimeRegister(0, exposure_val)
        else:
            self.control.SetIntegrationTimeMS(0, exposure_time)

    def set_image_dtype(self, N_bits=8):
        if N_bits == 8:
            dtype = DEVICE.Controller.COLOR_MODE.MONO8
        elif N_bits == 10:
            dtype = DEVICE.Controller.COLOR_MODE.MONO10
        elif N_bits == 12:
            dtype = DEVICE.Controller.COLOR_MODE.MONO12
        elif N_bits == 14:
            dtype = DEVICE.Controller.COLOR_MODE.MONO14
        elif N_bits == 16:
            dtype = DEVICE.Controller.COLOR_MODE.MONO16
        else:
            print("Number of bits not in allowed values, defaulting to 16-bit.")
            dtype = DEVICE.Controller.COLOR_MODE.MONO16
        self.control.SetColorMode(0, dtype)
        #print("dtype", dtype, "bits")

    def _save_image(self, filename="tmp", fileformat="txt"):
        if fileformat == "txt":
            AE.SWP800018.Processing.Codecs.TEXT.Save(self.camera.Image, filename+".txt")
        elif fileformat == "png":
            self.camera.Image.SaveImage(filename+".png")
        else:
            print(f"File format {fileformat} not recognized. Defaulting to TXT.")
            self._save_image(filename=filename, fileformat="txt")

       # ImageProcessing.SaveImage(cam_image, image_dir + f"\\rawCamera_{type_str}.png")
            
    def _capture_image(self):
        self._save_image(filename="tmp", fileformat="txt")
        self.image = np.loadtxt("tmp.txt")
        os.remove("tmp.txt")

        # self.control.SetFrameModeGlobal(DEVICE.Controller.FRAME_MODE_GLOBAL_FLAGS.FRAME_EN)
        # self.control.SetHeaderFooterMode(0,DEVICE.Controller.HEADER_FOOTER_MODE_FLAGS.NONE)
        # self.control.SetInputMode(0,DEVICE.Controller.INPUT_MODE.NORMAL)

        # # Set gain and expsoure settings
        # self.control.SetAGCMode(0, 1) # Set Auto-Gain mode to Manual
        # self.control.SetAGCGain(0, 3)
        # self.control.SetAGCOffset(0, 0)
        # self.control.SetAECMode(0, 0)
        # self.control.SetIntegrationTimeRegister(0, 9)
        #self.camera.Image.SaveImage(r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment\im" +".png")
        

    def return_image(self):
        self._capture_image()
        print("returning image")
        return self.image
    
    def save_image(self, filename, fileformat="png"):
        self._save_image(filename, fileformat)

    def return_image_mean(self):
        self._capture_image()
        return np.mean(self.image)

    def return_image_statistics(self):
        self._capture_image()
        return (np.mean(self.image), np.std(self.image))

    def close(self):
        self.camera.Close()
        self.control.ControlInterface.Close()
