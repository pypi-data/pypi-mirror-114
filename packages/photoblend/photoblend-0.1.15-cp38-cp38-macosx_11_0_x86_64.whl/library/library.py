from PIL import Image
from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap
import numpy as np
import ctypes
import os.path
import glob


def call_blend(image1_name, image2_name, blend_type):
    # Loads the shared object created by the Makefile (for pip install in WSL)
    # sofile = "blendlib.cpython-38-x86_64-linux-gnu.so"
    sofile = glob.glob('./*.so')[0]
    sopath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', sofile))
    _lib = ctypes.CDLL(sopath)

    # To run locally
    #dll_name = "blendlib.so"
    # dll_name = glob.glob('./*.so')[0]
    # dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
    # _lib = ctypes.CDLL(dllabspath)

    # Sets argument and return types for C functions
    _lib.AdditionBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.AdditionBlend.restype = None

    _lib.SubtractionBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.SubtractionBlend.restype = None

    _lib.MultiplicationBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.MultiplicationBlend.restype = None

    _lib.ScreenBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.ScreenBlend.restype = None

    _lib.OpacityBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.OpacityBlend.restype = None

    _lib.RedChannelBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.RedChannelBlend.restype = None

    _lib.GreenChannelBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.GreenChannelBlend.restype = None

    _lib.BlueChannelBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.BlueChannelBlend.restype = None

    _lib.OverlayBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.OverlayBlend.restype = None

    _lib.LightenBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.LightenBlend.restype = None

    _lib.DarkenBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.DarkenBlend.restype = None

    _lib.ColorDodgeBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.ColorDodgeBlend.restype = None

    _lib.ColorBurnBlend.argtypes = [
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C'),
        np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags='C')
    ]
    _lib.ColorBurnBlend.restype = None

    # Functions to bridge Python to C functions
    def addition_blend(size, image1, image2, result):
        _lib.AdditionBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def subtraction_blend(size, image1, image2, result):
        _lib.SubtractionBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def multiplication_blend(size, image1, image2, result):
        _lib.MultiplicationBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def screen_blend(size, image1, image2, result):
        _lib.ScreenBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def opacity_blend(size, image1, image2, result):
        _lib.OpacityBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def red_channel_blend(size, image1, image2, result):
        _lib.RedChannelBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def green_channel_blend(size, image1, image2, result):
        _lib.GreenChannelBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def blue_channel_blend(size, image1, image2, result):
        _lib.BlueChannelBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def overlay_blend(size, image1, image2, result):
        _lib.OverlayBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def lighten_blend(size, image1, image2, result):
        _lib.LightenBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def darken_blend(size, image1, image2, result):
        _lib.DarkenBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def color_dodge_blend(size, image1, image2, result):
        _lib.ColorDodgeBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    def color_burn_blend(size, image1, image2, result):
        _lib.ColorBurnBlend(ctypes.c_int(width1 * height1 * 3), image1, image2, result)

    # Open images/get dimensions
    try:
        img1 = Image.open(str(image1_name))
        width1, height1 = img1.size
    except FileNotFoundError as error:
        print('File ' + str(image1_name) + ' not found.')
        return
    except:
        print('Error other than file not found.')
        return

    try:
        img2 = Image.open(str(image2_name))
        width2, height2 = img2.size
    except FileNotFoundError as error:
        print('File ' + str(image2_name) + ' not found.')
        return
    except:
        print('Error other than file not found.')
        return

    # Create blank image object with same dimensions
    img3 = Image.new(mode="RGB", size=(height1, width1))

    # Convert the images to a 1-D numpy array
    image1 = np.asarray(img1).flatten()
    image2 = np.asarray(img2).flatten()
    image3 = np.asarray(img3).flatten()

    size = image1.size

    # Image details
    # print("Flat image Details:")
    # print("-------------------")
    # print(f"Dimensions: {image1.ndim}")
    # print(f"Shape: {image1.shape}")
    # print(f"Data Type: {image1.dtype}")
    # print(f"Object type: {type(image1)}")
    # print(f"CTypes: {image1.ctypes}\n")

    # call to C
    if blend_type == "add":
        addition_blend(size, image1, image2, image3)
    elif blend_type == "subtract":
        subtraction_blend(size, image1, image2, image3)
    elif blend_type == "multiply":
        multiplication_blend(size, image1, image2, image3)
    elif blend_type == "screen":
        screen_blend(size, image1, image2, image3)
    elif blend_type == "opacity":
        opacity_blend(size, image1, image2, image3)
    elif blend_type == "redchannel":
        red_channel_blend(size, image1, image2, image3)
    elif blend_type == "greenchannel":
        green_channel_blend(size, image1, image2, image3)
    elif blend_type == "bluechannel":
        blue_channel_blend(size, image1, image2, image3)
    elif blend_type == "overlay":
        overlay_blend(size, image1, image2, image3)
    elif blend_type == "lighten":
        lighten_blend(size, image1, image2, image3)
    elif blend_type == "darken":
        darken_blend(size, image1, image2, image3)
    elif blend_type == "color_dodge":
        color_dodge_blend(size, image1, image2, image3)
    elif blend_type == "color_burn":
        color_burn_blend(size, image1, image2, image3)
    else:
        print('Selected mode not currently supported.')
        return

    # Change resulting image back to 3-D array
    new_image = np.reshape(image3, (height1, width1, 3))
    result = Image.fromarray(new_image, 'RGB')
    result.save('test_image.jpg', 'JPEG')

    myImage = QLabel().setPixmap(QPixmap("test_image.jpg"))
    return myImage

    print("New image loaded.")
