import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as sp_fft
from scipy.ndimage import gaussian_filter




# Load your arrays

periods = np.array([80, 160, 240, 320, 400])
i = 4
path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
im = np.load(path+f"\grating_{periods[i]}um_test_0.npy")
M = -150/25.4

p = 240

x_offset = -1.225
X, Y = np.meshgrid(
    np.linspace(-6.4/2, 6.4/2, 1280),
    np.linspace(-5.12/2, 5.12/2,  1024))
X *= M
Y *= M
X -= x_offset
mask = (X**2 + Y**2 <= 2.5**2)
im[mask] = 1e-9


int_img = np.sum(im, axis = 0)

n_p = min(20, int_img.size)
top_n_indices_p = np.argsort(im.flatten())[-n_p:]

plt.scatter(X.flatten()[top_n_indices_p], Y.flatten()[top_n_indices_p], marker = "s", c = 'g')
plt.contourf(X, Y, im, levels=100, cmap="inferno", extend='both')
plt.axvline(0)
plt.xlabel('X [$mm$]', fontsize=14)
plt.ylabel('Y [$mm$]', fontsize=14)
plt.show()

print(top_n_indices_p)

plt.scatter(X.flatten()[top_n_indices_p], Y.flatten()[top_n_indices_p], marker = "s", c = 'g')
plt.plot(X[0], int_img)
plt.show()

print((X.flatten()[top_n_indices_p], Y.flatten()[top_n_indices_p]))

print("mean:",np.mean(np.abs(X.flatten()[top_n_indices_p])))

delta_x = np.array([14.53891758448099,8.075380341433084,4.348773586648033,3.3922275748565043, 3.3])


def linear_diff(lamb, p, z):
    return lamb/p*z
delta_x_t = linear_diff(1550*1e-6, periods*1e-3, 763)
plt.xlabel("linear grating periods [um]")
plt.ylabel("avrg deflection from center [mm]")
plt.scatter(periods,delta_x_t, label = "theory")
plt.scatter(periods, delta_x, label = "measured")
plt.grid()
plt.legend()
plt.show()

plt.plot(periods, np.abs((delta_x_t-delta_x))/delta_x_t*100)
plt.xlabel("linear grating periods [um]")
plt.ylabel("relative error from theory [%]")
plt.show()

ani = False
if ani:

    # # 1. Setup path and steps
    # path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
    rot_steps = np.linspace(-5_000, 5_000, 101)
    x_tra_steps = np.linspace(-5_000, 5_000, 51)
    sigma_value = 20
    file_name = f"\g1_x_tra_"
    im_noise = np.load(path+r"\noise.npy")
    empty_beam = np.load(path+r"\empty_beam_0.npy")
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
file_name = f"\g1_rot_"

# file_name = f"\g1_y_tra_"
# file_name = f"\\tra_z_g1_-50000.0_g2_-50000.0.0"
empty_beam = np.load(path+r"\empty_beam_0.npy")
im_noise = np.load(path+r"\noise.npy")
# plt.imshow(empty_beam)
#plt.show()
data = gaussian_filter(np.load(path + file_name + "0.0" +  ".npy") - empty_beam, sigma=sigma_value)
data = np.load(path + file_name + "0.0" + ".npy") - empty_beam
# plt.imshow(np.load(path + file_name + ".npy"))
# plt.title("2PGMI")
# plt.show()
# plt.plot(np.sum(np.load(path + file_name + ".npy"), axis = 0))
# plt.title("2PGMI")
# plt.show()



# plt.imshow(np.load(path + file_name + ".npy") - im_noise)
# plt.title("2PGMI - noise")
# plt.show()
# plt.plot(np.sum(np.load(path + file_name + ".npy") - im_noise, axis = 0))
# plt.title("2PGMI - noise")
# plt.show()

# plt.imshow(np.load(path + file_name + ".npy") - im_noise - empty_beam)
# plt.title("2PGMI - noise - empty_beam")
# plt.show()

# plt.plot(np.sum(np.load(path + file_name + ".npy")  - im_noise - empty_beam, axis = 0))
# plt.title("2PGMI - noise - empty_beam")
# plt.show()

# plt.plot(np.sum(np.load(path + file_name + ".npy") - empty_beam, axis = 0))
# plt.title("2PGMI - empty_beam")
# plt.show()

# # data = np.load(path + file_name + ".npy")- im_noise
# plt.plot(np.sum(data, axis = 0))
# plt.title("2PGMI - noise - empty_beam, Gussian filter")
# plt.show()
#data = np.load(path + r"\test3.npy")

data = data

# # print(np.shape(data))

# # plt.imshow(data)
# # plt.show()

# # M = 150/25.4


# X, Y = np.meshgrid(
#     np.linspace(-6.4/2, 6.4/2, 640),
#     np.linspace(-5.12/2, 5.12/2,  512))

# def plot_func(data, X, Y, title):


#     # Plot setup
#     cmap = 'inferno'
#     #fig, ax = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)

#     plt.contourf(X, Y, data, levels=100, cmap=cmap, extend='both')
#     plt.xlabel('X [$mm$]', fontsize=14)
#     plt.ylabel('Y [$mm$]', fontsize=14)
#     # plt.axvline(0.123)
#     plt.title("D = " + title, fontsize=16)
#     #fig.colorbar(cf, ax=ax)
#     #plt.xl

#     plt.show()

# plot_func(data, X, Y, "Test1")
# #plot_func(data-im_noise, X, Y, "Test1")
# plt.plot(X[0],data[0])
# plt.show()
# x = X[0] 
# freqs = sp_fft.fftshift(sp_fft.fftfreq(len(x), d=(x[1]-x[0])))
# plt.plot(freqs, np.abs(sp_fft.fftshift(sp_fft.fft(data[0]))))
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as sp_fft

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

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import scipy.fft as sp_fft
# from scipy.ndimage import gaussian_filter

# # --- User Configuration ---
# # Ensure these are defined in your environment
# # path = "your/file/path/" 
# # im_noise = np.load("noise_file.npy") 
# # pM = 100 # Define your pixel scaling factor if not already defined

# sigma_value = 20
# file_prefix = "tra_z_"

# # --- Grid Setup ---
# nx = 1280
# ny = 1024
# x = np.linspace(-6.4/2, 6.4/2, nx)
# y = np.linspace(-5.12/2, 5.12/2, ny)
# freqs = sp_fft.fftshift(sp_fft.fftfreq(len(x), d=(x[1]-x[0])))

# # --- Generate File List & Titles (The Sequence Logic) ---
# file_list = []
# title_list = []

# # Range: 50,000 to -50,000 in steps of 2000
# # Note: -50001 is used as 'stop' to ensure -50000 is included
# scan_range = np.arange(50_000, -50_001, -2_000)

# # PART 1: Vary G1 (50k -> -50k), Fix G2 (50k)
# for g1_pos in scan_range:
#     # Format: tra_z_g1_50000.0_g2_50000.0.npy
#     fname = f"\\{file_prefix}g1_{g1_pos:.1f}_g2_50000.0.npy"
#     tname = f"Translation step G1 = {g1_pos:.1f}, G2 = 50000.0"
    
#     file_list.append(fname)
#     title_list.append(tname)

# # PART 2: Fix G1 (-50k), Vary G2 (50k -> -50k)
# # Note: Prompt mentioned these files have a "type" (typo) ending in .0.0.npy
# for g2_pos in scan_range:
#     # Format: tra_z_g1_-50000.0_g2_50000.0.0.npy (Note the extra .0 based on prompt)
#     fname = f"\\{file_prefix}g1_-50000.0_g2_{g2_pos:.1f}.0.npy"
#     tname = f"Translation step G1 = -50000.0, G2 = {g2_pos:.1f}, d = {7+(0.25e-4*g2_pos):.2f}"
    
#     file_list.append(fname)
#     title_list.append(tname)

# # --- Figure setup ---
# fig, (ax_img, ax_fft) = plt.subplots(1, 2, figsize=(13, 5))

# # Load Initial Frame (Index 0)
# try:
#     # Construct full path. Note: Use / or \\ depending on OS, handled here generically
#     init_path = f"{path}{file_list[0]}"
#     data0_raw = np.load(init_path)
#     data0 = gaussian_filter(data0_raw - im_noise, sigma=sigma_value)
# except FileNotFoundError:
#     print(f"File not found: {file_list[0]}. Generating dummy data for setup.")
#     #data0 = np.random.rand(ny, nx) # Dummy data if file is missing during test

# intensity0 = np.sum(data0, axis=0)
# fft0 = np.abs(sp_fft.fftshift(sp_fft.fft(intensity0)))

# # Plot Initial Image
# im = ax_img.imshow(
#     data0,
#     extent=[x.min(), x.max(), y.min(), y.max()],
#     origin="lower",
#     cmap="inferno",
#     aspect="auto"
# )
# ax_img.set_title("2D Intensity")
# ax_img.set_xlabel("X [mm]")
# ax_img.set_ylabel("Y [mm]")

# # Plot Initial FFT
# line_fft, = ax_fft.plot(freqs, fft0, color='red')
# ax_fft.set_title("Fourier Transform")
# ax_fft.set_xlabel("Spatial Frequency [mm$^{-1}$]")
# ax_fft.set_ylabel("Magnitude")
# ax_fft.set_xlim(-4, 4)
# ax_fft.set_ylim(0, 1.1 * fft0.max())
# ax_fft.grid(alpha=0.3)
# if 'pM' in locals():
#     ax_fft.axvline(1/pM, label="Expected frequency", ls=":")
# ax_fft.legend()

# main_title = fig.suptitle(title_list[0])
# plt.tight_layout()

# # --- Update function ---
# def update(frame_idx):
#     current_file = file_list[frame_idx]
#     current_title = title_list[frame_idx]
    
#     try:
#         # Load file
#         full_path = f"\\{path}{current_file}"
#         data_raw = np.load(full_path)
        
#         # Process
#         data = gaussian_filter(data_raw - im_noise, sigma=sigma_value)
#         intensity = np.sum(data, axis=0)
#         fft_vals = np.abs(sp_fft.fftshift(sp_fft.fft(intensity)))

#         # Update plots
#         im.set_data(data)
#         line_fft.set_ydata(fft_vals)
        
#         # Dynamic Y-limit scaling for FFT (Optional, keeps plot clean)
#         # ax_fft.set_ylim(0, 1.1 * fft_vals.max()) 
        
#         main_title.set_text(current_title)
        
#     except FileNotFoundError:
#         print(f"Frame {frame_idx}: File {current_file} not found.")
        
#     return im, line_fft, main_title

# # --- Create Animation ---
# # frames set to len(file_list) ensures we iterate through the exact list we created
# ani = animation.FuncAnimation(
#     fig, 
#     update, 
#     frames=len(file_list), 
#     interval=100, # 100ms between frames
#     blit=False
# )

# # --- Save ---
# # ani.save(f"{path}animation_scan.gif", writer='pillow', fps=2)
# plt.show()


fourier_ani = False
if fourier_ani:
    import matplotlib.animation as animation
    import scipy.fft as sp_fft
    from scipy.ndimage import gaussian_filter

    # --- Animation parameters ---
    rot_steps = np.linspace(-5_000, 5_000, 101)
    x_tra_steps =  np.linspace(-10_000, 10_000, 51)
    # y_tra_steps =  np.linspace(-10_000, 10_000, 51)
    y_tra_steps = rot_steps
    z_tra_steps = np.linspace(-10_000, 10_000, 51)
    sigma_value = 20

    nx = 1280
    ny = 1024
    x = np.linspace(-6.4/2, 6.4/2, nx)
    y = np.linspace(-5.12/2, 5.12/2, ny)
    freqs = sp_fft.fftshift(sp_fft.fftfreq(len(x), d=(x[1]-x[0])))

    # --- Figure setup ---
    fig, (ax_img, ax_fft) = plt.subplots(1, 2, figsize=(13, 5))

    # Initial frame
    # data0 = gaussian_filter(
    #     np.load(path + file_name+f"{y_tra_steps[0]}.npy")-empty_beam,
    #     sigma=sigma_value
    # )
    data0 = np.load(path + file_name+f"{y_tra_steps[0]}.npy")-empty_beam
    

    intensity0 = np.sum(data0, axis = 0)
    fft0 = np.abs(sp_fft.fftshift(sp_fft.fft(intensity0)))
    X, Y = np.meshgrid(x,y)
    im = ax_img.imshow(
        data0,
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower",
        cmap="inferno",
        aspect="auto",
    vmin = 0)
    line_fft, = ax_fft.plot(freqs, fft0, color='red')

    ax_img.set_title("2D Intensity")
    ax_img.set_xlabel("X [mm]")
    ax_img.set_ylabel("Y [mm]")

    ax_fft.set_title("Fourier Transform")
    ax_fft.set_xlabel("Spatial Frequency [mm$^{-1}$]")
    ax_fft.set_ylabel("Magnitude")
    ax_fft.set_xlim(-4, 4)
    ax_fft.set_ylim(0, 1.1 * fft0.max())
    ax_fft.grid(alpha=0.3)
    ax_fft.axvline(1/pM, label = "Expected frequency", ls = ":")
    ax_fft.legend()

    title = fig.suptitle(f"Translation step = {y_tra_steps[0]:.0f}")

    plt.tight_layout()

    # --- Update function ---
    def update(frame):
        data = np.load(path + f"\g1_rot_{y_tra_steps[frame]}.npy") - empty_beam
        # data = gaussian_filter(np.load(path + f"\g1_rot_{y_tra_steps[frame]}.npy") - empty_beam, sigma=sigma_value)


        intensity = np.sum(data, axis=0)
        fft_vals = np.abs(sp_fft.fftshift(sp_fft.fft(intensity)))

        im.set_data(data)
        line_fft.set_ydata(fft_vals)
        ax_fft.set_ylim(0, 1.1 * fft_vals.max())
        title.set_text(f"rotation step = {y_tra_steps[frame]:.0f}")

        return im, line_fft, title

    # --- Create animation ---
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(y_tra_steps),
        interval=100,
        blit=False
    )

    # --- Save ---
    ani.save("fourier_vs_rotation.gif", writer="pillow", fps=2)

    plt.show()


# import numpy as np
# import scipy.fft as sp_fft
# from scipy.signal import find_peaks

# def first_physical_fft_peak(
#     intensity,
#     x,
#     f_min=0.1,
#     sigma_thresh=5.0,
#     window=True,
# ):
#     """
#     Finds the first non-zero physical spatial frequency peak in a 1D FFT.

#     Parameters
#     ----------
#     intensity : (N,) array
#         1D intensity profile (e.g. sum over y of 2D image)
#     x : (N,) array
#         Spatial coordinate in mm
#     f_min : float, optional
#         Minimum spatial frequency (mm^-1) to ignore DC / envelope effects
#     sigma_thresh : float, optional
#         Detection threshold in units of noise sigma
#     window : bool, optional
#         Apply Hann window before FFT

#     Returns
#     -------
#     f_peak : float
#         First non-zero physical spatial frequency (mm^-1)
#     amp_peak : float
#         FFT magnitude at the peak
#     fft_vals : ndarray
#         Full FFT magnitude spectrum
#     freqs : ndarray
#         Corresponding frequency axis
#     """

#     # --- DC removal ---
#     intensity = intensity - np.mean(intensity)

#     # --- Optional windowing ---
#     if window:
#         intensity = intensity * np.hanning(len(intensity))

#     # --- FFT ---
#     dx = x[1] - x[0]
#     freqs = sp_fft.fftshift(sp_fft.fftfreq(len(intensity), d=dx))
#     fft_vals = np.abs(sp_fft.fftshift(sp_fft.fft(intensity)))

#     # --- Exclude low-frequency region ---
#     valid = np.abs(freqs) > f_min

#     # --- Noise estimation ---
#     noise_floor = np.median(fft_vals[valid])
#     noise_sigma = np.std(fft_vals[valid])

#     threshold = noise_floor + sigma_thresh * noise_sigma

#     # --- Peak detection ---
#     peaks, props = find_peaks(
#         fft_vals,
#         height=threshold,
#         distance=5
#     )

#     # --- Select first positive-frequency peak ---
#     physical_peaks = peaks[freqs[peaks] > f_min]

#     if len(physical_peaks) == 0:
#         raise RuntimeError("No physical FFT peak found above noise threshold.")

#     idx = physical_peaks[0]

#     return freqs[idx], fft_vals[idx], fft_vals, freqs

# max_fs = []
# for i in rot_steps:
#     # Load data
#     #print(i)
#     im_data = gaussian_filter(np.load(path + f"\g1_rot_{i}.npy"), sigma=sigma_value)
#     nx = 1280
#     x = np.linspace(-6.4/2, 6.4/2, nx)
#     f_peak, amp_peak , _, _ = first_physical_fft_peak(np.sum(im_data, axis=0), x, 0.1)
#     print(f_peak)
#     max_fs.append(f_peak)


# plt.plot(rot_steps,max_fs)
# plt.show()
