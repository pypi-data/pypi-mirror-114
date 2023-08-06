#!/usr/bin/env python
import codefast as cf
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.keras.models import Sequential

from psox.measure import metrics
from psox.keras.postprocess import get_binary_prediction


def lstm_touchstone(X_train, y_train, X_test, y_test, input_dim:int):
    '''Quickly test of Naive Bayes effect'''
    cf.info('Touchstone on LSTM model.')
    max_length_sequence = max([len(e) for e in X_train])
    
    M = Sequential()
    M.add(Embedding(input_dim, 32, input_length=max_length_sequence))
    M.add(LSTM(100))
    M.add(Dropout(0.4))
    M.add(Dense(20, activation="relu"))
    M.add(Dropout(0.3))
    M.add(Dense(1, activation="sigmoid"))

    M.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])
    M.summary()
    M.fit(X_train, y_train, epochs=3, validation_split=0.1, batch_size=16)

    y_pred = get_binary_prediction(M.predict(X_test))
    metrics(y_test, y_pred)
