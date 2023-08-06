import logging
import numpy as np

from albumentations.core.transforms_interface import ImageOnlyTransform


class Normalize(ImageOnlyTransform):
    r"""Performs Normalization on the image
    
    Normalization is applied by the formula: 
    
    .. math:: img = \frac{img - mean}{std}

    Parameters
    ----------
    mean : list
        channel mean values
    std : list
        channel std values
    max_pixel_value : float
        maximum possible pixel value
    """    

    def __init__(self, mean=(0.485, 0.456, 0.406),
                 std=(0.229, 0.224, 0.225), always_apply=False, p=1.0):
        super(Normalize, self).__init__(always_apply, p)
        self.mean = np.array(mean, dtype=np.float32)
        self.std = np.array(std, dtype=np.float32)

    def apply(self, image, **params):
        logging.debug("Enter Normalize apply routine")
        denominator = np.reciprocal(self.std, dtype=np.float32)

        img = np.array(image, dtype=np.float32)
        img -= self.mean
        img *= denominator

        return img

    def get_transform_init_args_names(self):
        return ("mean", "std")

class MinMaxNormalize(ImageOnlyTransform):
    r"""Performs MinMax Normalization on the image.

    MinMax Normalization is applied by the formula :  
    
    .. math:: img = \frac{img - min}{max - min}

    Parameters
    ----------
    min : list
        band wise minimum values
    max : list
        band wise maximum values
    """    

    def __init__(self, min,max, always_apply=False, p=1.0):
        super(MinMaxNormalize, self).__init__(always_apply, p)
        self.min = np.array(min, dtype=np.float32)
        self.max = np.array(max, dtype=np.float32)

    def apply(self, image, **params):
        logging.debug("Enter MinMax Normalize apply routine")
        denominator = np.reciprocal(self.max - self.min, dtype=np.float32)

        img = np.array(image, dtype=np.float32)
        img -= self.min
        img *= denominator

        return img

    def get_transform_init_args_names(self):
        return ("min", "max")
