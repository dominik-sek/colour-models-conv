from skimage import io
from skimage.color import rgb2yuv
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

rgb = io.imread('../src/lena.png')
yuv = rgb2yuv(rgb)
y = yuv[:, :, 0]
u = yuv[:, :, 2]
v = yuv[:, :, 1]

# convert to uint8
io.imsave("../src/y.jpg", y)
io.imsave("../src/u.jpg", u)
io.imsave("../src/v.jpg", v)
io.imsave("../src/yuv.jpg", yuv)

plt.figure(0)

fig, axs = plt.subplots(1)

axs.hist(y.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("y Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("yYuvHist.png")

plt.figure(1)

fig, axs = plt.subplots(1)

axs.hist(u.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("u Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("uYuvHist.png")

plt.figure(2)

fig, axs = plt.subplots(1)

axs.hist(v.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("v Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("vYuvHist.png")
