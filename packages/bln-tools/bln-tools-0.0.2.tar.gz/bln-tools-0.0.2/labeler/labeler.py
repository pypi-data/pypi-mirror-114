import pickle
import random

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
import pandas as pd


class LabelError(Exception):
    pass


class Labeler:
    def __init__(
        self,
        texts: 'list[str]',
        labels: 'list[str]',
        mutually_exclusive_labels=False,
    ):
        assert len(labels) == len(set(labels)), 'Labels must be unique!'
        self.unlabeled = set([str(t) for t in texts if t])
        self.labels = sorted(labels)
        self.label_cols = self.labels
        self.mutually_exclusive_labels = mutually_exclusive_labels
        if self.mutually_exclusive_labels:
            self.label_cols = ['label']
        self.labeled = pd.DataFrame(columns=self.label_cols + ['text'])
        self.model = None

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def save(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self, f)

    def save_csv(self, path):
        self.labeled.to_csv(path, index=False)

    @property
    def n_reviewed(self):
        '''Returns the total number of reviewed items.'''
        return len(self.labeled)

    @property
    def n_remaining(self):
        '''Returns the total number left to review.'''
        return len(self.unlabeled)

    @property
    def n_distinct(self):
        '''Returns the total number of distinct texts.'''
        return self.n_reviewed + self.n_remaining

    def review(self, n=100):
        '''Returns a pandas dataframe to review.'''
        to_label = random.sample(self.unlabeled, min(n, len(self.unlabeled)))
        to_label = [str(v) for v in to_label]
        df = pd.DataFrame(columns=self.label_cols)
        if self.model:
            df = pd.DataFrame(self.model.predict(to_label),
                              columns=self.label_cols)
        df['text'] = to_label
        return df

    def update(self, review):
        '''Update labeler with reviewed dataframe.'''
        self.labeled = self.labeled.append(review)
        # drop duplicates, keeping the most recently added
        self.labeled.drop_duplicates('text', keep='last', inplace=True)
        self.unlabeled -= {r for r in review.text}

    def label_remainder_automatically(self):
        '''Label the remainder of the texts using model predictions.'''
        if not self.model:
            raise LabelError('Insufficient labeled texts.')
        self.update(self.review(n=self.n_remaining))

    def train(self):
        '''Trains the model when possible.'''
        if self.mutually_exclusive_labels or all(
                self.labeled[self.label_cols].sum() > 0):
            self.model = make_pipeline(
                CountVectorizer(analyzer='char_wb',
                                ngram_range=(2, 4),
                                stop_words='english',
                                lowercase=True),
                RandomForestClassifier(n_estimators=100))
            if self.mutually_exclusive_labels:
                self.model.fit(self.labeled.text, self.labeled.label.values)
            else:
                self.model.fit(self.labeled.text,
                               self.labeled[self.label_cols].astype('int'))

    def predict(self, texts):
        '''Uses current model to predict on given texts.'''
        if not self.model:
            raise LabelError('Insufficient labeled texts.')
        df = pd.DataFrame(self.model.predict(texts), columns=self.label_cols)
        df['text'] = texts
        return df
