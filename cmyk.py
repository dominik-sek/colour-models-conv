from PIL import Image
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
 
# Open image, convert to CMYK and save as PNG
Image.open('./web/src/imgs/lena.jpg').convert('CMYK').save('./web/src/imgs/lenaCmyk.jpeg', 'jpeg')
 
# lenaRGB = io.imread('./lena.png')
lenaCmyk = io.imread('./web/src/imgs/lenaCmyk.jpeg')
#cmykTest = io.imread('./web/src/imgs/cmykTest.jpg')
 
#print("This image has %d channels."%Image.open("./lenaCmyk.jpeg").layers)

lenaCyan = lenaCmyk.copy()
lenaCyan[:, :, 0] = 0
 
Image.fromarray(lenaCyan).save('./web/src/imgs/converted/lenaC.jpeg')

lenaMagenta = lenaCmyk.copy()
lenaMagenta[:, :, 1] = 0
Image.fromarray(lenaMagenta).save('./web/src/imgs/converted/lenaM.jpeg')

lenaYellow = lenaCmyk.copy()
lenaYellow[:, :, 2] = 0

Image.fromarray(lenaYellow).save('./web/src/imgs/converted/lenaY.jpeg')

lenaBlack = lenaCmyk.copy()
lenaBlack[:, :, 0] = 0
lenaBlack[:, :, 1] = 0
lenaBlack[:, :, 2] = 0
Image.fromarray(lenaBlack).save('./web/src/imgs/converted/lenaK.jpeg')
