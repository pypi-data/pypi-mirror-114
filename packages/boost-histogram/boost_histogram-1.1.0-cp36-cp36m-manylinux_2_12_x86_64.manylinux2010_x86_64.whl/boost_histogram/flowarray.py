# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from ..accumulators import Mean, WeightedMean, WeightedSum

import numpy as np

class FlowArray(np.ndarray):
    __slots__ = ()

    def __repr__(self):
        # Numpy starts the ndarray class name with "array", so we replace it
        # with our class name
        return (
            "{self.__class__.__name__}(\n      ".format(self=self)
            + repr(self.view(np.ndarray))[6:]
        )

