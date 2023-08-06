import numpy as np
import torch


def is_numpy(x):
    if type(x).__module__ == "numpy":
        return True
    return False

ii = torch.tensor(1j,dtype=torch.cfloat)
# abstract math functions if we need to stop using numpy
PI = np.pi
EXP = lambda x: np.exp(x) if is_numpy(x) else torch.exp(x)
SQRT = lambda x: np.sqrt(x) if is_numpy(x) else torch.sqrt(x)
SIN = lambda x: np.sin(x) if is_numpy(x) else torch.sin(x) 
COS = lambda x: np.cos(x) if is_numpy(x) else torch.cos(x) 
REAL_PART = lambda x: np.real(x) if is_numpy(x) else torch.real(x) 
CONJUGATE = lambda x: np.conj(x) if is_numpy(x) else torch.conj(x) 
LOG_10 = lambda x: np.log10(x) if is_numpy(x) else torch.log10(x)
POW_2 = torch.pow