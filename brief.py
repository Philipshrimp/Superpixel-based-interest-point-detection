from skimage import io

from skimage.feature import BRIEF
from skimage.color import rgb2gray

import numpy

def BRIEF_descriptor(filename, intermediate_point):
    print("Making BRIEF descriptors...")

    # Load image and descriptor
    input = rgb2gray(io.imread(filename))
    extractor = BRIEF()

    # Convert 'list' to 'numpy.ndarray'
    intermediate_point_array = numpy.array(intermediate_point)

    # Descriptor extraction
    extractor.extract(input, intermediate_point_array)
    descriptors = extractor.descriptors

    return descriptors