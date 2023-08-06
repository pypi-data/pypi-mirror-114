
from PIL import ImageGrab

def get_color_name(r, g, b):
    if r < 15 and g < 15 and b < 15:
        return "black"
    elif r > 220 and g > 220 and b > 220:
        return "white"
    elif r < g and g > 120 and b < g:
        return "green"
    elif r > 120 and g < r and b < r:
        return "red"
    elif r < b and g < b and b > 120:
        return "blue"
    elif r > 95 and g > 95 and b < 60:
        return "yellow"
    else:
        return "unknown"

def get_pixel_color(x, y):
    '''Returns RGB data from the given pixel coordinates'''
    return ImageGrab.grab(bbox=(x, y, x + 1, y + 1)).getdata()[0]

def get_pixel_color_name(x, y):
    '''Returns the name of a color at the given pixel coordinates'''
    color = get_pixel_color(x, y)
    return get_color_name(*color)
