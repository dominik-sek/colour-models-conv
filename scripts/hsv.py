from skimage import io
from skimage.color import rgb2hsv
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

rgb = io.imread('../src/lena.png')
hsv = rgb2hsv(rgb)
hue = hsv[:, :, 0]
value = hsv[:, :, 2]
sat = hsv[:, :, 1]

# convert to uint8
io.imsave("../src/hue.jpg", hue)
io.imsave("../src/val.jpg", value)
io.imsave("../src/sat.jpg", sat)
io.imsave("../src/hsv.jpg", hsv)

plt.figure(1)

fig, axs = plt.subplots(1)

axs.hist(hsv.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("HSV Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("hsvHist.png")

plt.figure(2)

fig, axs = plt.subplots(1)

axs.hist(hue.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("Hue Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("hueHist.png")

plt.figure(3)

fig, axs = plt.subplots(1)

axs.hist(value.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("Value Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("valueHist.png")

plt.figure(4)

fig, axs = plt.subplots(1)

axs.hist(sat.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("Sat Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("satHist.png")
