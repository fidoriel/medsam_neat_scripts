import os
import sys
import re
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2
 
'''
Load a PFM file into a Numpy array. Note that it will have
a shape of H x W, not W x H. Returns a tuple containing the
loaded image and the scale factor from the file.
'''
 
 
def load_pfm(file):
    color = None
    width = None
    height = None
    scale = None
    endian = None
 
    header = file.readline().rstrip().decode('UTF-8')
    #print(header)
    if header == 'PF':
        color = True
    elif header == 'Pf':
        color = False
    else:
        raise Exception('Not a PFM file.')
 
    dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline().decode('UTF-8'))
    if dim_match:
        width, height = map(int, dim_match.groups())
    else:
        raise Exception('Malformed PFM header.')
 
    scale = float(file.readline().decode('UTF-8').rstrip())
    if scale < 0:  # little-endian
        endian = '<'
        scale = -scale
    else:
        endian = '>'  # big-endian
 
    data = np.fromfile(file, endian + 'f')
    shape = (height, width, 3) if color else (height, width)
    return np.reshape(data, shape), scale
 
if len(sys.argv)==1:
    print('Usage: {} scale [files]'.format('pfmToPng'))
    sys.exit()
 
scale_factor = int(sys.argv[1])
temp = sys.argv[2:]
files = []
for f in temp:
    if os.path.exists(f):
        files.append(f)
    else:
        print('Skipping {}, file not found'.format(f))
 
for i,f in enumerate(files):
    with open(f,'rb') as f_in:
        disp, scale = load_pfm(f_in)
        disp[np.where(disp>0)]=0
        disp = scale_factor * np.flipud(disp)
        disp = disp.astype(np.uint16)
        cv2.imwrite(f.replace('.pfm','.png'),disp)
        print('{}/{}'.format(i,len(files)),end='\r')
        # pippo = Image.open(path)
        # plt.imshow(pippo)
        # plt.show()
    os.remove(f)
print('DONE!')