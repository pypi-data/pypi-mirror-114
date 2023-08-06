import codefast as cf
import numpy as np
from numpy.lib.arraypad import pad


def tokenize(X: list, return_processor: bool = False) -> list:
    cf.info(f'Tokenizing texts')
    from keras.preprocessing.text import Tokenizer
    tok = Tokenizer()
    tok.fit_on_texts(X)
    ans = tok.texts_to_sequences(X)
    return (ans, tok) if return_processor else ans


def label_encode(y: list, return_processor: bool = False) -> np.ndarray:
    '''Encode labels into 0, 1, 2...'''
    cf.info(f'Getting binary labels. Return encoder is set to {return_processor}')
    from sklearn.preprocessing import LabelEncoder
    enc = LabelEncoder()
    y_categories = enc.fit_transform(y)
    return (y_categories, enc) if return_processor else y_categories


def onehot_encode(y: list, return_processor: bool = False) -> np.ndarray:
    '''input format: y =[['red'], ['green'], ['blue']]
    '''
    cf.info(
        f'Getting one hot encode labels. Return encoder is set to {return_processor}'
    )
    assert isinstance(y[0], list) or isinstance(y[0], np.ndarray)
    from sklearn.preprocessing import OneHotEncoder
    enc = OneHotEncoder()
    y_categories = enc.fit_transform(y)
    return (y_categories, enc) if return_processor else y_categories

def pad_sequences(sequences, **kwargs):
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    seq = pad_sequences(sequences, **kwargs)
    return seq

