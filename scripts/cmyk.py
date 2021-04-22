from PIL import Image
from skimage import io
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np

# Open image, convert to CMYK and save as PNG
Image.open('../src/lena.png').convert('CMYK').save('../src/lenaCmyk.jpeg', 'jpeg')

# lenaRGB = io.imread('./lena.png')
lenaCmyk = io.imread('../src/lenaCmyk.jpeg')
# cmykTest = io.imread('./web/src/imgs/cmykTest.jpg')

# print("This image has %d channels."%Image.open("./lenaCmyk.jpeg").layers)


lenaCyan = lenaCmyk.copy()
lenaCyan[:, :, 0] = 0

Image.fromarray(lenaCyan).save('../src/lenaC.jpeg')

lenaMagenta = lenaCmyk.copy()
lenaMagenta[:, :, 1] = 0
Image.fromarray(lenaMagenta).save('../src/lenaM.jpeg')

lenaYellow = lenaCmyk.copy()
lenaYellow[:, :, 2] = 0

Image.fromarray(lenaYellow).save('../src/lenaY.jpeg')

lenaBlack = lenaCmyk.copy()

lenaBlack = lenaBlack - lenaMagenta
lenaBlack = lenaBlack - lenaCyan
lenaBlack = lenaBlack - lenaYellow

# lenaBlack.astype(np.uint8)
# height, width = lenaCmyk.size

# pixdata = lenaBlack.load()

# for loop1 in range(height):
#   for loop2 in range(width):
#      c, m, y = pixdata[loop1, loop2]
#    pixdata[loop1, loop2] = 0, m, y


Image.fromarray(lenaBlack).save('../src/lenaK.jpg')

plt.figure(1)

fig, axs = plt.subplots(1)

axs.hist(lenaCmyk[:, :, 1].ravel() + lenaCmyk[:, :, 0].ravel(), bins=256, color='yellow', alpha=0.5)
axs.set_title("Yellow Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("cmykHistYellow.png")

plt.figure(2)

fig, axs = plt.subplots(1)

axs.hist(lenaCmyk[:, :, 1].ravel() + lenaCmyk[:, :, 2].ravel(), bins=256, color='Cyan', alpha=0.5)
axs.set_title("Cyan Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("cmykHistCyan.png")

plt.figure(3)

fig, axs = plt.subplots(1)

axs.hist(lenaCmyk[:, :, 2].ravel() + lenaCmyk[:, :, 0].ravel(), bins=256, color='Magenta', alpha=0.5)
axs.set_title("Magenta Channel")
axs.set_ylabel("Count")
axs.set_xlabel("Intensity")

plt.savefig("cmykHistMagenta.png")

