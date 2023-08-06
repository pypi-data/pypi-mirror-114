import codefast as cf
import numpy as np
from numpy.lib.arraypad import pad


def datainfo(sequences: list) -> None:
    len_list = list(map(len, sequences))

    def percentile(n: int):
        return int(np.percentile(len_list, n))

    print('{:<30} {}'.format('Size of sequence:', len(sequences)))
    print('{:<30} {}'.format('Maximum length:', max(len_list)))
    print('{:<30} {}'.format('Minimum length:', min(len_list)))
    print('{:<30} {}'.format('Percentile 90 :', percentile(90)))
    print('{:<30} {}'.format('Percentile 80 :', percentile(80)))
    print('{:<30} {}'.format('Percentile 20 :', percentile(20)))
    print('{:<30} {}'.format('Percentile 10 :', percentile(10)))


def gpu_check():
    import tensorflow as tf
    tf.Session(config=tf.ConfigProto(
        log_device_placement=True)).run(tf.constant(1) + tf.constant(1))


def tokenize(X: list, return_processor: bool = False) -> list:
    cf.info(f'Tokenizing texts')
    from tensorflow.keras.preprocessing.text import Tokenizer
    tok = Tokenizer()
    tok.fit_on_texts(X)
    ans = tok.texts_to_sequences(X)
    return (ans, tok) if return_processor else ans


def label_encode(y: list, return_processor: bool = False) -> np.ndarray:
    '''Encode labels into 0, 1, 2...'''
    cf.info(
        f'Getting binary labels. Return encoder is set to {return_processor}')
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
