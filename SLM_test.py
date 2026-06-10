import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


print("AAAAAAAAAAAAAAAAAAA")

def generate_binary_cubic_phase_mask(size=512, alpha=50.0, filename="binary_cubic_mask.png"):
    """
    Generates and saves a binary blazed cubic phase mask for an SLM.

    Parameters:
    - size (int): The resolution of the square mask (e.g., 512 for a 512x512 SLM).
    - alpha (float): The strength/modulation factor of the cubic phase.
    - filename (str): The path where the output image will be saved.
    """
    
    # 1. Create a normalized 2D coordinate grid from -1 to 1
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)
    
    # 2. Calculate the continuous cubic phase profile
    # Formula: phase = alpha * (x^3 + y^3)
    continuous_phase = alpha * (X**3 + Y**3)
    
    # 3. "Blaze" the phase by wrapping it modulo 2*pi
    blazed_phase = np.mod(continuous_phase, 2 * np.pi)
    
    # 4. Binarize the phase
    # Threshold at pi: values < pi become 0, values >= pi become 1
    binary_phase = np.where(blazed_phase < np.pi, 0, 1)
    
    # 5. Scale to 8-bit integer (0 and 255) for SLM display
    slm_image_data = (binary_phase * 255).astype(np.uint8)
    
    # 6. Convert to an image and save
    # plt.imshow(slm_image_data)
    # plt.show()
    img = Image.fromarray(slm_image_data, mode='L')
    img.save(filename)
    
    print(f"Successfully saved {size}x{size} mask to '{filename}'.")
    print(f"Parameters used -> Alpha: {alpha}")

# Example usage:
if __name__ == "__main__":
    # Adjust 'size' to match your SLM's resolution (e.g., 1080 or 1920)
    # Adjust 'alpha' to change the density of the fringes
    generate_binary_cubic_phase_mask(size=1024, alpha=100.0, filename="slm_test_mask.png")