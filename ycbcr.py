from skimage import io
from PIL import Image
import numpy as np

rgb = io.imread('./web/src/imgs/lena.jpg')
r = rgb[:,:,0]
y = np.zeros_like(r)
Cb = np.zeros_like(r)
Cr = np.zeros_like(r)
