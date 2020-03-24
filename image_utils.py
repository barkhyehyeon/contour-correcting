import math
import numpy as np
import imageio
import cv2
from skimage import morphology, filters
from scipy import ndimage
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

def load_image(path):
    return imageio.imread(path)

def save_image(path, image):
    cv2.imwrite(path, image)
    
def remove_small_objects(image, threshold):
    image = image > 0
    ret = morphology.remove_small_objects(image, min_size=threshold, connectivity=1, in_place=False)
    return ret * 255

def leave_biggest_only(image):
    '''
    ref: https://stackoverflow.com/questions/56589691/how-to-leave-only-the-largest-blob-in-an-image
    '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Generate intermediate image; use morphological closing to keep parts of the brain together
    inter = cv2.morphologyEx(image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

    # Find largest contour in intermediate image
    cnts, _ = cv2.findContours(inter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cnts, key=cv2.contourArea)

    # Output
    out = np.zeros(image.shape, np.uint8)
    cv2.drawContours(out, [cnt], -1, 255, cv2.FILLED)
    out = cv2.bitwise_and(image, out)
    
    # fill holes
    out = out / 255
    out = ndimage.binary_fill_holes(out)*255
    return out

def find_convexhull(image):
    return morphology.convex_hull_image(image)

def center_of_mass(image):
    p = ndimage.measurements.center_of_mass(image)
    p = (int(round(p[0])), int(round(p[1])))
    return p

def detect_edge(image):
    padded = np.pad(image, ((1,1),(1,1)), 'constant')
    selem = morphology.disk(1)
    edge_padded = (filters.rank.minimum(padded, selem) == 0) & (filters.rank.maximum(padded, selem) == 255)
    return edge_padded[1:-1, 1:-1]

def rotate_point(center,point,angle):
    '''
    ref: https://gist.github.com/somada141/d81a05f172bb2df26a2c
    Rotates a point around another centerPoint. Angle is in degrees. Rotation is counter-clockwise.
    '''
    angle = math.radians(angle)
    temp_point = point[0]-center[0] , point[1]-center[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+center[0] , temp_point[1]+center[1]
    return temp_point

def remove_duplicate(a, b):
    c = a[:1]
    d = b[:1]
    for i in range(1, len(a)):
        if c[-1] != a[i] or d[-1] != b[i]:
            c = np.append(c, a[i])
            d = np.append(d, b[i])
    return c, d
        
def point_to_integer(a):
    b = [int(round(i)) for i in a]
    return np.array(b)

def trim_boundary(a):
    ret = []
    for i in a:
        if i < 0:
            ret.append(0)
        elif i > 511:
            ret.append(511)
        else:
            ret.append(i)
    return np.array(ret)

def spline_interpolate(a): 
    # a: input
    tck, u = splprep(a.T, u=None, s=0.0, per=1) 
    u_new = np.linspace(u.min(), u.max(), 2048)
    x_new, y_new = splev(u_new, tck, der=0)
    x_int, y_int = point_to_integer(x_new), point_to_integer(y_new)
    x_trim, y_trim = trim_boundary(x_int), trim_boundary(y_int)
    x_final, y_final = remove_duplicate(x_trim, y_trim)
    return x_final, y_final 

def floodfill_image(edge_x, edge_y, start_point, color):
    new_image = np.zeros((512, 512))
    for i in range(len(edge_x)):
        new_image[edge_x[i], edge_y[i]] = color
        
    mask = np.pad(new_image, ((1,1),(1,1)), 'constant')
    mask = np.uint8(mask)
    new_image = np.float32(new_image)
    cv2.floodFill(new_image, mask, (start_point[1], start_point[0]), color)
    return new_image

def show_image(image1):
    plt.imshow(image1, cmap='gray')
    
def overlap_image(image1, image2):
    plt.imshow(image1, cmap='gray')
    plt.imshow(image2, cmap='jet', alpha=0.5)
