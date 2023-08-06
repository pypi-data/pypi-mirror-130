"""These modules will allow you to analyze labeled and unlabeled tubulin - microtubulin time to catastrophe data.
compare_model assess the gamma distribution and two-step model
ecdf_tubulin generates a ECDF plot with confidence intervals for our labeled and unlabeled data
param_gamma finds and plots our parameter estimates for the gamma distribution
"""

from .compare_model import *
from .ecdf_tubulin import *
from .param_gamma import *

__author__ = 'Andres Rodriguez and Adiel Perez'
__email__ = 'amrodrig@caltech.edu and afperez@caltech.edu'
__version__ = '0.0.1'
__license__ = 'MIT'