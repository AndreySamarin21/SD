import pickle
import numpy as np
import nltk
nltk.download()

from abc import ABC, abstractmethod
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from operator import itemgetter


class BaseTagger(ABC):
    @abstractmethod
    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', 'text1_tag2', ...], ...]"""
        pass


class SGDClassifierTagger(BaseTagger):
    def __init__(self, threshold, filename_with_weights="model_weights.pik"):

        self.threshold = threshold
        self.pipeline = Pipeline(
            [('vect', CountVectorizer()),
             ('tfidf', TfidfTransformer()),
             ('SGDClassifier', SGDClassifier(learning_rate='adaptive',
                                             eta0=0.1,
                                             loss='modified_huber',
                                             penalty='elasticnet',
                                             tol=1e-5,
                                             max_iter=50,
                                             early_stopping=True,
                                             random_state=7576))])

        twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
        self.targets = twenty_test.target_names

        try:
            self.classifier = pickle.load(open(filename_with_weights, 'rb'))
            print("Uh-huh, the model is already trained")

        except FileNotFoundError:
            print("Oops, it's time to practice")
            twenty_train = fetch_20newsgroups(subset='train', shuffle=True)

            parameters = {'SGDClassifier__alpha': np.linspace(0.00001, 0.0001, 2)}
            cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

            self.grid_pipeline = GridSearchCV(self.pipeline, parameters, cv=cv)
            self.grid_pipeline.fit(twenty_train.data, twenty_train.target)
            self.classifier = self.grid_pipeline.best_estimator_.fit(twenty_train.data, twenty_train.target)
            self.classifier = self.classifier.fit(twenty_train.data, twenty_train.target)
            predictions = self.classifier.predict(twenty_test.data)

            print(f"Accuracy:{np.mean(predictions == twenty_test.target):.2f}")

            pickle.dump(self.classifier, open(filename_with_weights, 'wb'))

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', 'text1_tag2', ...], ...]"""
        tags = []
        scores = []
        for text in texts:
            predictions = self.classifier.predict_proba([text])[0].tolist()
            sorted_scores = [(predictions[i], predictions.index(predictions[i])) for i in range(len(predictions))]
            sorted_scores = sorted(sorted_scores, reverse=True, key=itemgetter(0))
            valid_predictions = []
            valid_predictions_scores = []

            for v in range(len(sorted_scores)):
                if sorted_scores[v][0] >= self.threshold:
                    valid_predictions.append(self.targets[sorted_scores[v][1]])
                    valid_predictions_scores.append(sorted_scores[v][0])
            tags.append(valid_predictions)
            scores.append(valid_predictions_scores)

        scores = [item for sublist in scores for item in sublist]
        scores = ['%.2f' % elem for elem in scores]
        return tags, scores


example = [
    "He people of Israel, having fled across the watery deep of the Red Sea with dryshod feet, beholding the mounted captains of the enemy drowned therein, sang with gladness: Let us chant unto our God, for He hath been glorified!",
    "The Civil War is one of the most studied and written about episodes in the history of the United States",
    'Fresh out of college, Elon Musk built his first business around an early Web search technology to help struggling newspapers launch themselves into the digital world'
]

tags, scores = SGDClassifierTagger(threshold=0.2).get_tags(example)

print("Predictions:\n", tags)
print(scores)





""""
Oops, it's time to practice
Accuracy:0.85
Predictions:
 [['talk.politics.mideast'], ['talk.politics.misc'], ['sci.space']]
['0.26', '0.27', '0.24']



Uh-huh, the model is already trained
Predictions:
 [['talk.politics.mideast'], ['talk.politics.misc'], ['sci.space']]
['0.26', '0.27', '0.24']

"""
