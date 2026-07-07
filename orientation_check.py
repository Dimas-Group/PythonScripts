import os
import PyCapture2
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- connect to camera ---
bus = PyCapture2.BusManager()
cam = PyCapture2.Camera()
cam.connect(bus.getCameraFromIndex(0))
cam.startCapture()

# --- grab one frame ---
raw = cam.retrieveBuffer()

# --- try to demosaic to a proper color image; fall back to raw mono ---
try:
    converted = raw.convert(PyCapture2.PIXEL_FORMAT.BGR)
    rows = converted.getRows()
    cols = converted.getCols()
    data = np.array(converted.getData(), dtype=np.uint8).reshape((rows, cols, 3))
    img_rgb = data[:, :, ::-1]  # BGR -> RGB for matplotlib
    is_color = True
except Exception as e:
    print("Color conversion failed, showing raw mono/Bayer data:", e)
    rows = raw.getRows()
    cols = raw.getCols()
    img_rgb = np.array(raw.getData(), dtype=np.uint8).reshape((rows, cols))
    is_color = False

cam.stopCapture()
cam.disconnect()

# --- save raw array for later numpy analysis ---
npy_path = os.path.join(SCRIPT_DIR, 'captured_frame.npy')
np.save(npy_path, img_rgb)
print(f'Saved raw array to {npy_path}')

# --- display full 2D image so orientation is visible ---
plt.figure()
plt.imshow(img_rgb, cmap=None if is_color else 'gray', origin='upper')
plt.xlabel('Column index (0 = left)')
plt.ylabel('Row index (0 = top)')
plt.title(f'Captured frame ({rows} rows x {cols} cols)')

plot_path = os.path.join(SCRIPT_DIR, 'orientation_check_plot.png')
plt.savefig(plot_path)
print(f'Saved plot to {plot_path}')

plt.show()
