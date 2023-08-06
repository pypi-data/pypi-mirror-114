#!/usr/bin/env python
import codefast as cf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from premium.measure import metrics


def touchstone(X: list, y: list, is_cn: bool = False):
    if is_cn:
        import jieba
        X = [' '.join(jieba.lcut(e)) for e in X]

    cv = CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b')
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        random_state=42,
                                                        test_size=0.2)
    X_train = cv.fit_transform(X_train)
    X_test = cv.transform(X_test)
    nb = MultinomialNB()
    nb.fit(X_train, y_train)
    y_pred = nb.predict(X_test)

    metrics(y_test, y_pred)
