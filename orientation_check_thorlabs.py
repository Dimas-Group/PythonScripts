import os
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from pylablib.devices import uc480

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(SCRIPT_DIR, 'thorlabs_camera_settings.tcp')

IS_PARAMETERSET_CMD_LOAD_FILE = 1


def load_camera_settings(cam, filepath):
    """Load a ThorCam-exported .tcp/.ini settings file onto the camera (same as ThorCam's Load button)."""
    raw = cam.lib.lib
    raw.is_ParameterSet.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
    raw.is_ParameterSet.restype = ctypes.c_int
    buf = ctypes.create_unicode_buffer(filepath)
    ret = raw.is_ParameterSet(cam.hcam, IS_PARAMETERSET_CMD_LOAD_FILE, ctypes.cast(buf, ctypes.c_void_p), 0)
    if ret != 0:
        raise RuntimeError(f'is_ParameterSet(LOAD_FILE) failed with code {ret}')


# --- connect to camera, apply saved settings, and grab one frame ---
cam = uc480.UC480Camera()
try:
    load_camera_settings(cam, SETTINGS_FILE)

    # Set exposure time (seconds).
    actual_exposure = cam.set_exposure(0.007)
    print(f'Exposure set to {actual_exposure} s (requested 0.007)')
    print(f'get_exposure() reports {cam.get_exposure()} s')

    # Discard a couple of frames: exposure changes take a frame or two to
    # fully apply on a rolling-shutter sensor, so the first grab(s) right
    # after set_exposure() can be a partial/transitional frame.
    cam.snap()
    cam.snap()
    frame = cam.snap()  # (rows, cols, 3) BGR for color cameras, (rows, cols) for mono
finally:
    cam.close()

if frame.ndim == 3:
    img_rgb = frame[:, :, ::-1]  # BGR -> RGB for matplotlib
    is_color = True
else:
    img_rgb = frame
    is_color = False

rows, cols = img_rgb.shape[:2]

# --- save raw array for later numpy analysis ---
npy_path = os.path.join(SCRIPT_DIR, 'captured_frame_thorlabs_on.npy')
np.save(npy_path, img_rgb)
print(f'Saved raw array to {npy_path}')

# --- display full 2D image so orientation is visible ---
plt.figure()
plt.imshow(img_rgb, cmap=None if is_color else 'gray', origin='upper')
plt.xlabel('Column index (0 = left)')
plt.ylabel('Row index (0 = top)')
plt.title(f'Captured frame ({rows} rows x {cols} cols)')

plot_path = os.path.join(SCRIPT_DIR, 'orientation_check_thorlabs_plot_on.png')
plt.savefig(plot_path)
print(f'Saved plot to {plot_path}')

plt.show()
