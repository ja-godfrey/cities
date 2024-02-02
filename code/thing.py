# %%
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c-(z/1.25)
    return max_iter

# Image size (pixels)
width, height = 800, 800

# Plot window
real_min, real_max = -0.5, 0.5
imag_min, imag_max = -0.5, 0.5

# Generating the Mandelbrot set
image = np.zeros((width, height))
for x in range(width):
    for y in range(height):
        real = real_min + x * (real_max - real_min) / width
        imag = imag_min + y * (imag_max - imag_min) / height
        color = mandelbrot(complex(real, imag), 40)
        image[x, y] = color

plt.imshow(image.T, extent=[real_min, real_max, imag_min, imag_max])
plt.colorbar()
plt.title("Mandelbrot Set")
plt.show()


# %%
