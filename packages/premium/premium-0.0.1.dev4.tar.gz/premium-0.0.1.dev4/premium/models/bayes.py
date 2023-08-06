#!/usr/bin/env python
import codefast as cf
from sklearn.naive_bayes import MultinomialNB

from premium.measure import metrics


# Refer https://www.kaggle.com/astandrik/simple-spam-filter-using-naive-bayes
def touchstone(X_train, y_train, X_test, y_test):
    '''Quickly test of Naive Bayes effect'''
    cf.info('Touchstone on Naive Bayes model.')
    M = MultinomialNB()
    M.fit(X_train, y_train)
    y_pred = M.predict(X_test)
    metrics(y_test, y_pred)
