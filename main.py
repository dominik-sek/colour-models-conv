import eel
import skimage.io
from skimage import io
from io import BytesIO
from skimage.color import rgb2hsv, rgb2yuv
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import base64
import re

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
        PIL_image.save(output_bytes, 'JPEG')
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

        hsv_64 = encode(hsv)
        hue_64 = encode(hue)
        value_64 = encode(value)
        sat_64 = encode(sat)

        list64 = {
            "HSV": [hsv_64],
            "Hue": [hue_64],
            "Value": [value_64],
            "Saturation": [sat_64]
        }

        return list64


def r2cmyk():
    while link_to_image is None:
        pass
    else:
        pass


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
        yuv_64 = encode(yuv)
        list64 = {  # list of base64 images
            "Luminance(Y)": [y_64],
            "Bandwidth(U)": [u_64],
            "Chrominance(V)": [v_64],
            "YUV": [yuv_64]
        }
        return list64


def r2r():  # rgb to components
    while link_to_image is None:
        pass
    else:
        image = link_to_image
        imagegreen = image.copy()
        imagegreen[:, :, 0] = 0
        imagegreen[:, :, 2] = 0

        imageblue = image.copy()
        imageblue[:, :, 0] = 0
        imageblue[:, :, 1] = 0

        imagered = image.copy()
        imagered[:, :, 1] = 0
        imagered[:, :, 2] = 0

        red_64 = encode(imagered)
        green_64 = encode(imagegreen)
        blue_64 = encode(imageblue)
        list64 = {  # list of base64 images
            "Red": [red_64],
            "Green": [green_64],
            "Blue": [blue_64],
        }

        return list64


###########################################################################

dispatcher = {
    'rgb2hsv': r2h,
    'rgb2cmyk': r2cmyk,
    'rgb2yuv': r2yuv,
    'rgb2rgb': r2r,
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
