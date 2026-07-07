import PyCapture2
import numpy as np
import matplotlib.pyplot as plt

# --- connect to camera ---
bus = PyCapture2.BusManager()
cam = PyCapture2.Camera()
cam.connect(bus.getCameraFromIndex(0))
cam.startCapture()

# --- grab one frame ---
img = cam.retrieveBuffer()
rows = img.getRows()
cols = img.getCols()
data = np.array(img.getData(), dtype=np.uint8).reshape((rows, cols))

cam.stopCapture()
cam.disconnect()

# --- horizontal line profile at a chosen row ---
row_index = rows // 2          # middle row; change to the row you want
profile = data[row_index, :]

plt.figure()
plt.plot(profile, 'k-')
plt.xlabel('Pixel Number')
plt.ylabel('Intensity')
plt.title(f'Horizontal Line Profile (row {row_index})')
plt.xlim(0, cols - 1)
plt.show()


#run using "C:\Users\pgmi2\AppData\Local\Programs\Python\Python36\python.exe" "c:\Users\pgmi2\camera_script\orientation_check.py"