from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg
from keras.preprocessing import image
import numpy as np
from numpy import linalg as LA
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
from werkzeug.utils import secure_filename
from keras.applications.vgg16 import VGG16
from common.const import input_shape
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.5
from vggnet import VGGNet
model = None
def load_model():

    global sess
    sess = tf.Session(config=config)
    set_session(sess)

    global graph
    graph = tf.get_default_graph()

    global model

    model = VGGNet()
    # model = VGG16(weights='imagenet',
    #               input_shape=input_shape,
    #               pooling='max',
    #               include_top=False)
    return model, graph, sess