from skimage import io, exposure
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


lena = io.imread('../src/lena.png')

# 0 - RED 1- GREEN 2-BLUE

lenagreen = lena.copy()
lenagreen[:, :, 0] = 0
lenagreen[:, :, 2] = 0
Image.fromarray(lenagreen).save('../src/lenaG.jpeg')

lenablue = lena.copy()
lenablue[:, :, 0] = 0
lenablue[:, :, 1] = 0
Image.fromarray(lenablue).save('../src/lenaB.jpeg')

lenared = lena.copy()
lenared[:, :, 1] = 0
lenared[:, :, 2] = 0
Image.fromarray(lenared).save('../src/lenaR.jpeg')

plt.figure(1)

fig, axs = plt.subplots(1)

# _ = plt.hist(lena[:, :, 0].ravel(), bins=256, color='red', alpha=0.5)
# _ = plt.hist(lena[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
# _ = plt.hist(lena[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)

axs.hist(lena[:, :, 0].ravel(), bins=256, color='red', alpha=0.5)
axs.set_title("Red Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("rgbHistRed.png")

plt.figure(2)

fig, axs = plt.subplots(1)

# _ = plt.hist(lena[:, :, 0].ravel(), bins=256, color='red', alpha=0.5)
# _ = plt.hist(lena[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
# _ = plt.hist(lena[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)

axs.hist(lena[:, :, 1].ravel(), bins=256, color='Green', alpha=0.5)
axs.set_title("Green Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("rgbHistGreen.png")

plt.figure(3)

fig, axs = plt.subplots(1)

# _ = plt.hist(lena[:, :, 0].ravel(), bins=256, color='red', alpha=0.5)
# _ = plt.hist(lena[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
# _ = plt.hist(lena[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)

axs.hist(lena[:, :, 2].ravel(), bins=256, color='Blue', alpha=0.5)
axs.set_title("Blue Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("rgbHistBlue.png")

plt.show()
