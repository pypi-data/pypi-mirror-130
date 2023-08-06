try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

## import required functions
import os
# ignore gpu: this needs to rectfied incase there is gpu access to tensorflow
# os.environ["CUDA_VISIBLE_DEVICES"]="-1" 
import tensorflow as tf
try:
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
    pass

import numpy as np
from skimage.transform import rescale,resize
from skimage.feature import shape_index
from skimage.util import random_noise

# import MiSiC Stuff
from misic_ui.misic.misic import *
from misic_ui.misic.extras import *
from misic_ui.misic.utils import *
# get helper functions
from misic_ui.misic_helpers import *

from napari_plugin_engine import napari_hook_implementation
from magicgui import magic_factory
from magicgui.tqdm import trange
from napari import Viewer
from napari.layers import Image

import pathlib
import json

# make misic
mseg = MiSiC()

def segment_single_image(im,params):
    sr,sc = im.shape
    tmp = preprocess(im,params)
    yp = mseg.segment(tmp,exclude = 16)
    yp = resize(yp,(sr,sc,2))
    yp = yp[:,:,0]
    return (yp*255).astype(np.uint8)

# make default params dictionary
params = {}
params['invert'] = True
params['scale'] = 1.0
params['gamma'] = 0.5
params['sharpness'] = 2
params['gaussian_laplace'] = False
params['sensitivity'] = 0.001
params['local_noise'] = True
params['post_process'] = True

mean_width = 12
standard_width = 12.0

@magic_factory(call_button='get_cell_width')
def get_width(viewer: Viewer):    
    '''
    Make a Shapes layer named 'cell_width' if it doesnt exists.
    Get the mean width of multiple lines to obtain the working scale
    '''
    standard_width = 12.0
    try:
        lines = viewer.layers['cell_width'].data       
    except:
        viewer.add_shapes([[[128,128],[128+(standard_width/1.414),128+(standard_width/1.414)]]], shape_type='line', edge_width=2, edge_color='coral', face_color='royalblue',name = 'cell_width')
        lines = viewer.layers['cell_width'].data
    mean_width = 0
    for l in lines:
        mean_width += np.sqrt((l[0][0]-l[1][0])**2 + (l[0][1]-l[1][1])**2)
    mean_width/=len(lines)
    params['scale'] = standard_width/mean_width
    

## MagicGui widget for single image segmentation
@magic_factory(auto_call=True,
adjust_scale = {"widget_type": "FloatSlider", "max": 1.2,"min": 0.8,"step":0.025,'tracking': False,'readout' : True}, 
gamma = {"widget_type": "FloatSlider", "max": 2.0,"min": 0.1,"step":0.1,'tracking': False,'readout' : True},
sharpness = {"widget_type": "FloatSlider", "max": 10,"min": 1,"step":0.5,'tracking': False,'readout' : True},
sensitivity = {"widget_type": "FloatSlider", "max": 0.50,"min": 0.00,"step":0.0001,'tracking': False,'readout' : True})
def segment(data: 'napari.types.ImageData', 
invert=True,
local_noise = False,
gaussian_laplace = False,
adjust_scale = 1,
gamma= 0.5,
sharpness = 2,
sensitivity = 0.0001, 
post_process= False) -> 'napari.types.ImageData':
    '''
    Get parameters for a single image and output segmented image.
    '''
    scale = min(standard_width/mean_width,2.5)*adjust_scale 
    params['invert'] = invert
    params['scale'] = scale
    params['gamma'] = gamma
    params['sharpness'] = sharpness
    params['gaussian_laplace'] = gaussian_laplace
    params['sensitivity'] = sensitivity
    params['local_noise'] = local_noise
    params['post_process'] = post_process
    
    if len(data.shape) >2:
        # frame_num = min(frame_num,len(data))
        im = np.copy(data[0])        
    else:
        im = np.copy(data)            
    #status = 'MiSiC: processing ...'
    yp = segment_single_image(im,params)    
    #status = 'MiSiC'
    return yp #Image(yp,name = 'segment result',opacity = 0.8, blending = 'additive', colormap = 'green')

# once the parameters are the selected for single image, then process the stack
@magic_factory()
def segment_stack(data: "napari.types.ImageData") -> Image:
    '''
    Segment the entire stack using the parameters obtained before
    '''
    params['scale'] = min(params['scale'],2.5)
        
    if len(data.shape) <3:
        yp = segment_single_image(np.copy(data),params)
    else:
        im = np.copy(data)
        yp = np.array([segment_single_image(im[i],params) for i in trange(len(im))])        
    return Image(yp,name = 'misic', opacity = 0.8, blending = 'additive', colormap = 'green')


############ Save or Load parameters file
@magic_factory(output_folder={'mode': 'd'},call_button='Save')
def save_params(output_folder =  pathlib.Path.home(),filename = 'params'):
    '''
    Save parameters to file
    '''
    output_folder = os.path.normpath(output_folder)
    filename = output_folder + os.path.sep + filename + '.json'
    
    json.dump( params, open( filename, 'w' ) )

@magic_factory(filename={'mode': 'r','filter':'.json'},call_button='Load')
def load_params(filename =  pathlib.Path.home()):
    '''
    Load parameters to file
    '''
    output_folder = os.path.normpath(output_folder)
    filename = output_folder + os.path.sep + filename + '.json'
    
    params = json.load( open( filename) )
    
############ napari hooks
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [get_width,segment,segment_stack,save_params,load_params]

