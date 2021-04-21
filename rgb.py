from skimage import io
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from PIL import Image

lena = io.imread('./web/src/imgs/lena.jpg')

#0 - RED 1- GREEN 2-BLUE

lenagreen = lena.copy()
lenagreen[:,:,0] = 0
lenagreen[:,:,2] = 0
Image.fromarray(lenagreen).save('./web/src/imgs/converted/lenaG.jpeg')


lenablue = lena.copy()
lenablue[:,:,0] = 0
lenablue[:,:,1] = 0
Image.fromarray(lenablue).save('./web/src/imgs/converted/lenaB.jpeg')


lenared = lena.copy()
lenared[:,:,1] = 0
lenared[:,:,2] = 0
Image.fromarray(lenared).save('./web/src/imgs/converted/lenaR.jpeg')

