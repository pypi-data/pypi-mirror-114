"""
Basic initialization for all processes in taskbench.
"""

from __future__ import print_function, absolute_import

# Publish information about this package Information
version_number = (1, 2, 1)
__version__ = version = ver = '%i.%i.%i' % version_number
revision = 'dev'
# github commit index
commit = ''

# Warnings
import warnings
warnings.filterwarnings("ignore")

# NumPy print options
import numpy as np
np.set_printoptions(precision=3)
