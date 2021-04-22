from skimage import io
from PIL import Image
import numpy as np
from skimage.color import rgb2ycbcr
import matplotlib.pyplot as plt

rgb = io.imread('../src/lena.png')
ycbcr = rgb2ycbcr(rgb)
y = ycbcr[:, :, 0]
cb = ycbcr[:, :, 1]
cr = ycbcr[:, :, 2]

io.imsave("../src/yTestt.jpg", y)
io.imsave("../src/cbTestt.jpg", cb)
io.imsave("../src/crTestt.jpg", cr)

plt.figure(0)

fig, axs = plt.subplots(1)

axs.hist(y.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("Y Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("yHist.png")

plt.figure(1)

fig, axs = plt.subplots(1)

axs.hist(cb.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("cb Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("cbHist.png")

fig, axs = plt.subplots(1)

axs.hist(cr.ravel(), bins=256, color='blue', alpha=0.5)
axs.set_title("cr Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("crHist.png")
