import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.fft as sp_fft
from scipy.ndimage import gaussian_filter
import os  # <--- Import os for safe path joining
path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
ani = False
if ani:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    # # 1. Setup path and steps
    # path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
    rot_steps = np.linspace(-5_000, 5_000, 101)
    x_tra_steps = np.linspace(-5_000, 5_000, 51)
    sigma_value = 20
    file_name = f"\g1_x_tra_"
    im_noise = np.load(path+r"\noise.npy")
    blurred_image = gaussian_filter(np.load(path + file_name + f"{rot_steps[25]}.npy"), sigma=sigma_value)
    plt.imshow(blurred_image)
    plt.show()
    # tra_y_step = np.linspace(-10_000, 10_000, 51)

    fig = plt.figure()
    frames = []
    # 2. Loop and store 'Artist' objects
    for i in rot_steps:
        # Load data
        im_data = gaussian_filter(np.load(path + f"\g1_rot_{i}.npy"), sigma=sigma_value)
        
        # Create the plot for this frame
        # Note: we use animated=True and store it in a list
        img = plt.imshow(im_data, animated=True)
        plt.axvline(320, color = "r")
        title = plt.text(0.5, 1.01, f"y_pos: {i}", 
                            ha="center", va="bottom", transform=plt.gca().transAxes)
        
        frames.append([img, title])

    # 3. Create the animation
    ani = animation.ArtistAnimation(fig, frames, interval=100, blit=True)

    # 4. Save the video
    # Note: You need ffmpeg installed on your system for .mp4
    ani.save('tra_y_alignment_video.gif', writer='pillow', fps=2)

    plt.show()


# # g1_pos_steps = np.arange(-50_000 , 50_000 + 5_000, 5_000)
# # g1_pos_cm = np.arange(-1, -3.5, 20)
# # i = 0
# # step = g1_pos_steps[i]
# # #for 
rot_steps = np.linspace(-5_000, 5_000, 101)
sigma_value = 20
# file_name = f"\g1_rot_"

# file_name = f"\g1_y_tra_"
#file_name = f"\\tra_z_g1_-50000.0_g2_-50000.0.0"
im_noise = np.load(path+r"\noise.npy")
data = gaussian_filter(np.load(path + file_name + ".npy") - im_noise, sigma=sigma_value)
# data = np.load(path + file_name + ".npy")- im_noise
plt.plot(np.sum(data, axis = 0))
plt.show()
#data = np.load(path + r"\test3.npy")

data = data
# --- User Configuration ---
# path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment" 
# im_noise = np.load("noise_file.npy") 
# pM = 100 


L = 76 #cm
L1 = 31.7 # cm
d = 7 # cm
pG = 180e-3 #mm
pM = L/d*pG
pA = 2*L*pG/(d+2*L1)
print("pM = ", pM, "mm")
print("pA = ", pA, "mm")

# Dimensions from your meshgrid setup
nx = 1280
ny = 1024
x = np.linspace(-6.4/2, 6.4/2, nx)
y = np.linspace(-5.12/2, 5.12/2, ny)
X, Y = np.meshgrid(x, y)

# Extracting a slice (using synthetic data for demonstration)
intensity_slice = np.sum(data, 0) # Your code used the first row
# intensity_slice = ... 

# Compute Fourier Transform
freqs = sp_fft.fftshift(sp_fft.fftfreq(len(x), d=(x[1]-x[0])))
fft_vals = np.abs(sp_fft.fftshift(sp_fft.fft(intensity_slice)))

# Plotting
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# # Intensity Plot
# im1 = ax1.contourf(X, Y, data, levels=100, cmap='inferno', vmin = 0)
# ax1.set_title('2D Intensity Distribution')
# ax1.set_xlabel('X [mm]')
# ax1.set_ylabel('Y [mm]')
# plt.colorbar(im1, ax=ax1)

# # FFT Plot
# ax2.plot(freqs, fft_vals, color='red')
# #ax2.set_xlim()
# ax2.set_xlabel('Spatial Frequency [mm$^{-1}$]')
# ax2.set_ylabel('Magnitude')
# ax2.set_title('Fourier Transform')
# ax2.set_xlim(-1e-9, 7) # Adjusted to show typical frequency ranges
# ax2.grid(True, alpha=0.3)

# plt.tight_layout()
# plt.show()


sigma_value = 40
file_prefix = "tra_z_"

# --- Grid Setup ---
nx = 1280
ny = 1024
x = np.linspace(-6.4/2, 6.4/2, nx)
y = np.linspace(-5.12/2, 5.12/2, ny)
freqs = sp_fft.fftshift(sp_fft.fftfreq(len(x), d=(x[1]-x[0])))

# --- Generate File List & Titles ---
file_list = []
title_list = []

scan_range = np.arange(50_000, -50_001, -2_000)

# PART 1: Vary G1 (50k -> -50k), Fix G2 (50k)
for g1_pos in scan_range:
    # REMOVED the "\\" at the start of fname
    fname = f"{file_prefix}g1_{g1_pos:.1f}_g2_50000.0.npy"
    tname = f"Translation step G1 = {g1_pos:.1f}, G2 = 50000.0, d = {7+(0.25e-4*(np.abs(g1_pos-50000))):.2f}"

    pM = L/(7+(0.25e-4*(np.abs(g1_pos-50000))))*pG
    
    file_list.append(fname)
    title_list.append(tname)

# PART 2: Fix G1 (-50k), Vary G2 (50k -> -50k)
for g2_pos in scan_range:
    # REMOVED the "\\" at the start of fname
    fname = f"{file_prefix}g1_-50000.0_g2_{g2_pos:.1f}.0.npy"
    tname = f"Translation step G1 = -50000.0, G2 = {g2_pos:.1f}, d = {7+(0.25e-4*np.abs((g2_pos-50000))):.2f}"
    pM = L/(7+(0.25e-4*(np.abs(g1_pos-50000))))*pG
    
    file_list.append(fname)
    title_list.append(tname)

# --- Figure setup ---
fig, (ax_img, ax_fft) = plt.subplots(1, 2, figsize=(13, 5))

# Load Initial Frame
try:
    # USE os.path.join for safe path construction
    init_path = os.path.join(path, file_list[0])
    data0_raw = np.load(init_path)
    data0 = gaussian_filter(data0_raw - im_noise, sigma=sigma_value)
except FileNotFoundError:
    print(f"File not found: {file_list[0]}")
    # Create dummy data so the plot doesn't crash if file is missing
    data0 = np.zeros((ny, nx))

intensity0 = np.sum(data0, axis=0)
fft0 = np.abs(sp_fft.fftshift(sp_fft.fft(intensity0)))

# Plot Initial Image
im = ax_img.imshow(
    data0,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="inferno",
    aspect="auto"
)
ax_img.set_title("2D Intensity")
ax_img.set_xlabel("X [mm]")
ax_img.set_ylabel("Y [mm]")

# Plot Initial FFT
line_fft, = ax_fft.plot(freqs, fft0, color='red')
ax_fft.set_title("Fourier Transform")
ax_fft.set_xlabel("Spatial Frequency [mm$^{-1}$]")
ax_fft.set_ylabel("Magnitude")
ax_fft.set_xlim(-4, 4)
ax_fft.set_ylim(0, 1.1 * (fft0.max() if fft0.max() > 0 else 1)) # Prevent 0 ylim error
ax_fft.grid(alpha=0.3)

if 'pM' in locals():
    ax_fft.axvline(1/pM, label="Expected frequency", ls=":")
ax_fft.legend()

main_title = fig.suptitle(title_list[0])
plt.tight_layout()

# --- Update function ---
def update(frame_idx):
    current_file = file_list[frame_idx]
    current_title = title_list[frame_idx]
    
    try:
        # USE os.path.join here as well
        full_path = os.path.join(path, current_file)
        
        data_raw = np.load(full_path)
        
        # Process
        data = gaussian_filter(data_raw - im_noise, sigma=sigma_value)
        intensity = np.sum(data, axis=0)
        fft_vals = np.abs(sp_fft.fftshift(sp_fft.fft(intensity)))

        # Update plots
        im.set_data(data)
        line_fft.set_ydata(fft_vals)
        
        main_title.set_text(current_title)
        
    except FileNotFoundError:
        print(f"Frame {frame_idx}: File {current_file} not found at {full_path}")
        
    return im, line_fft, main_title

# --- Create Animation ---
ani = animation.FuncAnimation(
    fig, 
    update, 
    frames=len(file_list), 
    interval=100, 
    blit=False
)

plt.show()