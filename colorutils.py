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
    print("image:", image)
    hsv = image[:,:,:3]
    print("hsv:", hsv)
    a = image[:,:,3:]
    hsv = hsv.clip(0,1)
    print("hsvclip:", hsv)
    a = a.clip(0,1)
    print("aclip:", hsv)
    rgb = color.hsv2rgb(hsv)
    a = a
    rgba = np.concatenate((rgb,a),axis=2) * 255.0
    print("rgba:", hsv)
    rgba = rgba.clip(0,255).astype(np.uint8)
    return rgba

def test():
    import matplotlib.pyplot as plt
    rgba = io.imread("debug.png")
    plt.figure(figsize=(20, 2))
    # plt.imshow(rgba,interpolation='nearest')
    plt.imshow(HSVAtoRGBA(RGBAtoHSVA(rgba)),interpolation='nearest')
    plt.show()
