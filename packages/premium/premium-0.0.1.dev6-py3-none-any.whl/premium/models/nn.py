#!/usr/bin/env python
import uuid
from re import VERBOSE

import codefast as cf
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.keras.models import Sequential

from premium.measure import metrics
from premium.postprocess import get_binary_prediction
from premium.preprocess import label_encode, pad_sequences, tokenize

tf.compat.v1.disable_eager_execution()


def optimal_batch_size(sequence_size: int) -> int:
    import math
    base = int(math.log(sequence_size + 1, 10))
    batch_size = 1 << (base + 2)
    cf.info('Batch size is set to ', batch_size)
    return batch_size


def _touchstone(X_train,
                y_train,
                X_test,
                y_test,
                input_dim: int,
                input_length: int = 300):
    '''Quickly test of Naive Bayes effect'''
    cf.info('Touchstone on LSTM model.')

    M = Sequential()
    M.add(Embedding(input_dim, 32, input_length=input_length))

    M.add(LSTM(100))
    M.add(Dropout(0.4))

    M.add(Dense(20, activation="relu"))
    M.add(Dropout(0.4))
    M.add(Dense(1, activation="sigmoid"))

    M.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])
    M.summary()

    weight_path = f'/tmp/best_weights_{uuid.uuid4()}.h5'
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
    checkpoint = ModelCheckpoint(weight_path,
                                 monitor='val_loss',
                                 save_weights_only=True,
                                 verbose=1,
                                 save_best_only=True,
                                 period=1)
    fit_params = {
        'batch_size': optimal_batch_size(len(X_train)),
        'validation_split': 0.15,
        'epochs': 45,
        'callbacks': [es, checkpoint]
    }
    M.fit(X_train, y_train, **fit_params)
    M.load_weights(weight_path)

    y_pred = get_binary_prediction(M.predict(X_test))
    metrics(y_test, y_pred)
    return M


def lstm_touchstone(X, y, is_cn: bool = False):
    import numpy as np

    if is_cn:
        import jieba
        X = [' '.join(jieba.lcut(e)) for e in X]
    y = label_encode(y)
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        random_state=42,
                                                        test_size=0.2)
    X_train, tok = tokenize(X_train, return_processor=True)
    X_test = tok.texts_to_sequences(X_test)
    max_length_sequence = int(np.percentile(list(map(len, X)), 80))
    cf.info('set max_length_sequence to', max_length_sequence)
    assert max_length_sequence >= 2, 'max length is less than 2, check your data.'

    X_train = pad_sequences(X_train, maxlen=max_length_sequence, padding="pre")
    X_test = pad_sequences(X_test, maxlen=max_length_sequence, padding="pre")

    input_dim = len(tok.word_index) + 1
    _touchstone(X_train,
                y_train,
                X_test,
                y_test,
                input_dim,
                input_length=max_length_sequence)
