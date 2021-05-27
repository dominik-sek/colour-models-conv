import eel
from skimage.color.colorconv import gray2rgb, hsv2rgb
import skimage.io
from skimage import io, exposure
from io import BytesIO
from skimage.color import rgb2hsv, rgb2yuv
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
import base64
import re

import cv2


eel.init("web")


def decode(base64_string):
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")

    imgdata = base64.b64decode(re.sub('^data:image/.+;base64,', '', base64_string))
    img = skimage.io.imread(imgdata, plugin="imageio")
    return img


def encode(image) -> str:
    with BytesIO() as output_bytes:
        PIL_image = Image.fromarray(skimage.img_as_ubyte(image))
        PIL_image.save(output_bytes, 'PNG')
        bytes_data = output_bytes.getvalue()

    base64_str = str(base64.b64encode(bytes_data), 'utf-8')

    return base64_str


@eel.expose
def link(self):
    while self is None:
        pass
    else:
        print("fired link")
        global link_to_image
        link_to_image = self
        link_to_image = decode(link_to_image)
        print("link to the image here: ", link_to_image)


# CONVERTING FUNCTIONS ##################################################

#RGB TO OTHERS
def r2h():
    while link_to_image is None:
        pass
    else:
        print("fired r2h")
        rgb = link_to_image
        hsv = rgb2hsv(rgb)
        hue = hsv[:, :, 0]
        value = hsv[:, :, 2]
        sat = hsv[:, :, 1]

        hue_64 = encode(hue)
        value_64 = encode(value)
        sat_64 = encode(sat)

        list64 = {
            "Hue": [hue_64],
            "Value": [value_64],
            "Saturation": [sat_64]
        }

        return list64

def r2cmyk():
    while link_to_image is None:
        pass
    else:
        image = Image.fromarray(link_to_image).convert('CMYK')
        np_image = np.array(image)

        c,m,y,k = cv2.split(np_image)
        print(c)

        
        cyan_64 = encode(c)
        magenta_64 = encode(m)
        yellow_64 = encode(y)
        bk_64 = encode(k)
        list64 = {  # list of base64 images
            "Cyan": [cyan_64],
            "Magenta": [magenta_64],
            "Yellow": [yellow_64],
            "Black": [bk_64],

        }
        return list64

def r2yuv():
    while link_to_image is None:
        pass
    else:
        image = link_to_image
        yuv = rgb2yuv(image)
        y = yuv[:, :, 0]
        u = yuv[:, :, 2]
        v = yuv[:, :, 1]

        y_64 = encode(y)
        u_64 = encode(u)
        v_64 = encode(v)
        list64 = {  # list of base64 images
            "Luminance(Y)": [y_64],
            "Bandwidth(U)": [u_64],
            "Chrominance(V)": [v_64],
        }
        return list64

def r2r(): 
    while link_to_image is None:
        pass
    else:
        image = link_to_image
        imagegreen = image.copy()
        imagegreen[:, :, 0] = 0
        imagegreen[:, :, 2] = 0
        plt.figure(1)
        fig, axs = plt.subplots(1)

        axs.hist(imagegreen.ravel(), bins=256, color='green', alpha=0.5)
        #config:
        axs.axis('off')
        fig.tight_layout(pad = 0)
        axs.margins(0)
        fig.canvas.draw()
        green_hist = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        #green_hist = green_hist.reshape(fig.canvas.get_width_height()[::-1]+(3,))

        imageblue = image.copy()
        imageblue[:, :, 0] = 0
        imageblue[:, :, 1] = 0

        plt.figure(1)
        fig, axs = plt.subplots(1)

        axs.hist(imageblue.ravel(), bins=256, color='blue', alpha=0.5)
        #config:
        axs.axis('off')
        fig.tight_layout(pad = 0)
        axs.margins(0)
        fig.canvas.draw()
        blue_hist = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        blue_hist = blue_hist.reshape(fig.canvas.get_width_height()[::-1]+(3,))


        imagered = image.copy()
        imagered[:, :, 1] = 0
        imagered[:, :, 2] = 0

        plt.figure(1)
        fig, axs = plt.subplots(1)

        axs.hist(imagered.ravel(), bins=256, color='red', alpha=0.5)
        #config:
        axs.axis('off')
        fig.tight_layout(pad = 0)
        axs.margins(0)
        fig.canvas.draw()
        red_hist = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        red_hist = red_hist.reshape(fig.canvas.get_width_height()[::-1]+(3,))


        red_64 = encode(imagered)
        red_hist_64 = encode(red_hist)

        green_64 = encode(imagegreen)
        green_hist_64 = encode(green_hist)

        blue_64 = encode(imageblue)
        blue_hist_64 = encode(blue_hist)

        list64 = {  # list of base64 images
            "Red": [red_64, red_hist_64],
            "Green": [green_64, green_hist_64],
            "Blue": [blue_64, blue_hist_64],
        }

        return list64
#ENDOF RGB TO OTHERS

# ###########################HSV###############################

#HSV TO OTHERS


def h2r():
    while link_to_image is None:
        pass
    else:
        print("fired h2r")
        hsv = link_to_image
        rgb = hsv2rgb(hsv)
        print(rgb)
        print("++=====++")
        print(hsv)

        red = rgb[:, :, 0]
        green = rgb[:, :, 2]
        blue = rgb[:, :, 1]



        red_64 = encode(red)
        green_64 = encode(green)
        blue_64 = encode(blue)

        list64 = {
            "Red": [red_64],
            "Green": [green_64],
            "Blue": [blue_64]
        }
        return list64


def h2h():
    pass
def h2cmyk():
    pass
def h2yuv():
    pass

#ENDOF HSV TO OTHERS

# ##########################CMYK###############################

#CMYK TO OTHERS 

def cmyk2r():
    pass
def cmyk2h():
    pass
def cmyk2cmyk():
    pass
def cmyk2y():
    pass

#ENDOF CMYK TO OTHERS

# ##########################YUV################################
#YUV TO OTHERS

def yuv2r():
    pass
def yuv2h():
    pass
def yuv2cmyk():
    pass
def yuv2y():
    pass
#ENDOF YUV TO OTHERS
# #############################################################





###########################################################################

dispatcher = {

    'rgb2hsv': r2h,
    'rgb2cmyk': r2cmyk,
    'rgb2yuv': r2yuv,
    'rgb2rgb': r2r,

    'hsv2rgb' : h2r,
    'hsv2hsv' : h2h,
    'hsv2cmyk' : h2cmyk,
    'hsv2yuv' : h2yuv,
    
    'cmyk2rgb' : cmyk2r,
    'cmyk2rgb' : cmyk2h,
    'cmyk2rgb' : cmyk2cmyk,
    'cmyk2rgb' : cmyk2y,

    'yuv2rgb' : yuv2r,
    'yuv2hsv' : yuv2h,
    'yuv2cmyk' : yuv2cmyk,
    'yuv2yuv' : yuv2y,



}


# @eel.expose
# def passImages(dispatcher):
# print("fired passImages ",)

#  return r2h()

@eel.expose
def which_fun(self):
    while self is None:
        pass
    else:
        print("fired typeof: ", self)
        # dispatcher[self]()
        return dispatcher[self]()


eel.start('index.html', size=(1200, 720))
