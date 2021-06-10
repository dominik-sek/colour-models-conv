import PIL
import eel
from skimage.color.colorconv import gray2rgb, hsv2rgb, rgb2gray
import skimage.io
from skimage import io, exposure,img_as_float
from io import BytesIO
from skimage.color import rgb2hsv, rgb2yuv
from PIL import Image, ImageCms

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
        rgb = link_to_image
        hsv = rgb2hsv(rgb)
        hue = hsv[:, :, 0]
        value = hsv[:, :, 2]
        sat = hsv[:, :, 1]

        huehist_64 = encode(makeHist(hue))
        hue_64 = encode(hue)

        value_64 = encode(value)
        valuehist_64 = encode(makeHist(value))

        sat_64 = encode(sat)
        sathist_64 = encode(makeHist(sat))

        hsv_64 = encode(hsv)
        hsvhist_64 = encode(makeHist(hsv))

        list64 = {
            "Hue": [hue_64, huehist_64],
            "Saturation": [sat_64, sathist_64],
            "Value": [value_64, valuehist_64],
            "HSV": [hsv_64, hsvhist_64]
        }

        return list64

def getCmyk(image):

    R = image[:,:,0].astype(float)
    G = image[:,:,1].astype(float)
    B = image[:,:,2].astype(float)
    
    C = np.zeros_like(B)
    M = np.zeros_like(B)
    Y = np.zeros_like(B)
    K = np.zeros_like(B)
    

    R_ =np.copy(R)
    G_ =np.copy(G)
    B_ =np.copy(B)


    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            R_[i, j] = R[i, j]/255
            G_[i, j] = G[i, j]/255
            B_[i, j] = B[i, j]/255

            K[i, j] = 1 - max(R_[i, j], G_[i, j], B_[i, j])
            if (R_[i, j] == 0) and (G_[i, j] == 0) and (B_[i, j] == 0):
            # black
                C[i, j] = 0
                M[i, j] = 0  
                Y[i, j] = 0
            else:
                C[i, j] = ((1 - B_[i, j] - K[i, j])/float((1 - K[i, j])))
                M[i, j] = ((1 - G_[i, j] - K[i, j])/float((1 - K[i, j])))
                Y[i, j] = ((1 - R_[i, j] - K[i, j])/float((1 - K[i, j])))

    CMYK = (np.dstack((C,M,Y,K)) * 255).astype(np.uint8)
    return CMYK



def r2cmyk():
    pass
    while link_to_image is None:
        pass
    else:
        image = link_to_image
        image_array = np.array
    image_cmyk = getCmyk(image)

    m = image_cmyk[:,:,0]
    c = image_cmyk[:,:,1]
    y = image_cmyk[:,:,2]
    k = image_cmyk[:,:,3]

    


    cyan_64 = encode(c)
    magenta_64 = encode(m)
    yellow_64 = encode(y)
    bk_64 = encode(k)
    chist = encode(makeHist(c))
    mhist = encode(makeHist(m))
    yhist = encode(makeHist(y))
    khist = encode(makeHist(k))

    

    list64 = {  # list of base64 images
            "Cyan": [cyan_64,chist],
            "Magenta": [magenta_64,mhist],
            "Yellow": [bk_64,khist],
            "black": [yellow_64,yhist],

    }
    return list64


def make_lut_u():
    return np.array([[[i,255-i,0] for i in range(256)]],dtype=np.uint8)

def make_lut_v():
    return np.array([[[0,255-i,i] for i in range(256)]],dtype=np.uint8)

def r2yuv():
    while link_to_image is None:
        pass
    else:
        image = link_to_image
        img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        y, u, v = cv2.split(img_yuv)
        lut_u, lut_v = make_lut_u(), make_lut_v()

        y = cv2.cvtColor(y, cv2.COLOR_GRAY2BGR)
        u = cv2.cvtColor(u, cv2.COLOR_GRAY2BGR)
        v = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)

        u_m = cv2.LUT(u, lut_u)
        v_m = cv2.LUT(v, lut_v)


        y_64 = encode(y)
        u_64 = encode(u_m)
        v_64 = encode(v_m)
        img_yuv_64 = encode(img_yuv)

        yhist_64 = encode(makeHist(y))
        uhist_64 = encode(makeHist(u_m))
        vhist_64 = encode(makeHist(v_m))

        list64 = {  # list of base64 images
            "Luminance(Y)": [y_64,yhist_64],
            "Bandwidth(U)": [u_64,uhist_64],
            "Chrominance(V)": [v_64,vhist_64],
            "YUV":[img_yuv_64,vhist_64]
        }
        return list64

def r2r(): 
    while link_to_image is None:
        pass
    else:
        image = link_to_image

        print(image[:,:,1][255])
        imagegreen = image.copy()
        imagegreen[:, :, 0] = 0
        imagegreen[:, :, 2] = 0


        greenhist = imagegreen.copy()
        greenhist = rgb2gray(greenhist)

    
        #green_hist = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        #green_hist = green_hist.reshape(fig.canvas.get_width_height()[::-1]+(3,))

        imageblue = image.copy()
        imageblue[:, :, 0] = 0
        imageblue[:, :, 1] = 0

        bluehist = imageblue.copy()
        bluehist = rgb2gray(bluehist)


        imagered = image.copy()
        imagered[:, :, 1] = 0
        imagered[:, :, 2] = 0

        redhist = imagered.copy()
        redhist = rgb2gray(redhist)



        red_64 = encode(imagered)
        red_hist_64 = encode(makeHist(redhist))##tu

        green_64 = encode(imagegreen)
        green_hist_64 = encode(makeHist(greenhist))##tu

        blue_64 = encode(imageblue)
        blue_hist_64 = encode(makeHist(bluehist))
        

#------------------------grayscale------------------------#
        rgbgray = link_to_image
        rgbgray = rgb2gray(rgbgray)


        rgbgray_64 = encode(rgbgray)
        gray_hist_64 = encode(makeHist(rgbgray))
        #blue_hist_64 = encode(blue_hist)


        list64 = {  # list of base64 images
            "Red": [red_64, red_hist_64],
            "Green": [green_64, green_hist_64],
            "Blue": [blue_64, blue_hist_64],
            "RGB to grayscale":[rgbgray_64, gray_hist_64]
        }

        return list64


def makeHist(colorspace):
    
        histogram,bin_edges = np.histogram(colorspace ,bins=256,range=(0,1))
        fig = plt.figure()
        plt.xlim([0.0,1.0])
        plt.plot(bin_edges[0:-1],histogram)
        
        fig.canvas.draw()
        w,h = fig.canvas.get_width_height()
        hist = np.fromstring(fig.canvas.tostring_argb(),dtype =np.uint8)
        hist.shape = (w,h,4)
        hist = np.roll(hist,3,axis=2)
        hist_i = Image.frombytes("RGBA",(w,h),hist.tostring())
        hist = np.asarray(hist_i)

        return hist
#ENDOF RGB TO OTHERS
def r2grayscale():
    pass

# ###########################HSV###############################



#HSV TO OTHERS

###deprecated methods###
def h2r():
    while link_to_image is None:
        pass
    else:
        print("fired h2r")
        hsv = link_to_image
        rgb = hsv2rgb(hsv)
        print("++=====++")

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
    #'rgb2grayscale': r2grayscale,

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
