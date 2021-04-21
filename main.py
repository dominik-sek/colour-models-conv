import eel
import skimage.io
from skimage import io
from io import BytesIO
from skimage.color import rgb2hsv
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
        global link_to_image
        link_to_image = self
        link_to_image = decode(link_to_image)
        print("link to the image here: ", link_to_image)

def r2h():
    while link_to_image is None:
        pass
    else:
        print("fired r2h")
        rgb = link_to_image
        hsv = rgb2hsv(rgb)
        hue = hsv[:,:,0]
        value = hsv[:,:,2]
        sat = hsv[:,:,1]

        hsv_64 = encode(hsv)
        hue_64 = encode(hue)
        value_64 = encode(value)
        sat_64 = encode(sat)
        #convert to uint8
       # io.imsave("./web/src/imgs/converted/hue.jpg",hue)
       # io.imsave("./web/src/imgs/converted/val.jpg",value)
     #   io.imsave("./web/src/imgs/converted/sat.jpg",sat)
     #   io.imsave("./web/src/imgs/converted/hsv.jpg",hsv)
        list64 = {
        "HSV":[hsv_64],
        "Hue":[hue_64],
        "Value":[value_64],
        "Saturation":[sat_64]
        }

        return list64

dispatcher = {
    'rgb2hsv':r2h,
}

@eel.expose
def passImages():
    print("fired passImages ",)
    return r2h()

@eel.expose
def which_fun(self):
    while self is None:
        pass
    else:
        print("fired typeof: ", self)
        dispatcher[self]()

eel.start('index.html', size=(1200, 720))
