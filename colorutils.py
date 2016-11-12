import numpy as np
from skimage import color
import skimage.io as io

def RGBAtoHSVA(image):
    rgb = image[:,:,:3]
    a = image[:,:,3:] / 255.0
    hsv = color.rgb2hsv(rgb)
    hsva = np.concatenate((hsv,a),axis=2)
    return hsva

def HSVAtoRGBA(image):
    # print("image:", image)
    hsv = image[:,:,:3]
    # print("hsv:", hsv)
    a = image[:,:,3:]
    hsv = hsv.clip(0,1)
    # print("hsvclip:", hsv)
    a = a.clip(0,1)
    # print("aclip:", hsv)
    rgb = color.hsv2rgb(hsv)
    a = a
    rgba = np.concatenate((rgb,a),axis=2) * 255.0
    # print("rgba:", hsv)
    rgba = rgba.clip(0,255).astype(np.uint8)
    return rgba

def test():
    rgba = io.imread("debug.png")
    hsva = RGBAtoHSVA(rgba)
    noise = np.random.normal(0,0.01,rgba.shape)
    hsva += noise
    io.imsave("debug_rgbaconvert.png", HSVAtoRGBA(hsva))
