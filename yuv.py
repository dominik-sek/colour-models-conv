from skimage import io
from skimage.color import rgb2yuv
from PIL import Image
import numpy as np

rgb = io.imread('./web/src/imgs/lena.jpg')
yuv = rgb2yuv(rgb)
y = yuv[:,:,0]
u = yuv[:,:,2]
v = yuv[:,:,1]

#convert to uint8
io.imsave("./web/src/imgs/converted/y.jpg",y)
io.imsave("./web/src/imgs/converted/u.jpg",u)
io.imsave("./web/src/imgs/converted/v.jpg",v)
io.imsave("./web/src/imgs/converted/yuv.jpg",yuv)

