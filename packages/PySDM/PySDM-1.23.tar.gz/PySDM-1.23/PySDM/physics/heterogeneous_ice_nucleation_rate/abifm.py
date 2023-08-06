import numpy as np
from ..constants import si

m = np.inf
c = np.inf
unit = 1 / si.cm**2 / si.s


class ABIFM:
    @staticmethod
    def _check():
        assert np.isfinite(m)
        assert np.isfinite(c)

    @staticmethod
    def j_het(a_w_ice):
        return 10**(m * (1 - a_w_ice) + c) * unit
