import sys

if sys.version_info < (3, 11):
    sys.exit(f"Can Python 3.11+, dang dung {sys.version.split()[0]}")

import numpy
import matplotlib

print("Python    :", sys.version.split()[0])
print("NumPy     :", numpy.__version__)
print("Matplotlib:", matplotlib.__version__)
print("Moi truong OK!")
