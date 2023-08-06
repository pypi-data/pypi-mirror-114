#!/usr/bin/env python
import codefast as cf
import numpy as np

def get_binary_prediction(y_pred: list, threshold: float = 0.5):
    cf.info(f'Get binary prediction of y_pred')
    ans = []
    for e in y_pred:
        if isinstance(e, int) or isinstance(e, float):
            assert 0 <= e <= 1
            ans.append(1 if e >= threshold else 0)
        elif isinstance(e, list) or isinstance(e, np.ndarray):
            assert len(e) == 1, 'item should contains only one number.'
            n_float = float(e[0])
            assert 0 <= n_float <= 1
            ans.append(1 if n_float >= threshold else 0)
        else:
            print(e, type(e))
            raise TypeError('Unsupported element type.')
    return ans
