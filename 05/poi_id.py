#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

features_list = ['poi', 'salary', 'total_payments', 'bonus', 'deferred_income',
                 'total_stock_value', 'expenses', 'exercised_stock_options', 'other',
                 'long_term_incentive', 'restricted_stock', 'to_messages', 
                 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi',
                 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
import pandas as pd
import numpy as np

df = pd.DataFrame.from_dict(data_dict, orient = 'index')
df = df.replace('NaN', np.nan)

df = df.drop(['TOTAL'])

### Task 3: Create new feature(s)
df['bonus_percent'] = df['salary']/df['total_payments']
df['poi_messages'] = df['from_poi_to_this_person']+df['from_this_person_to_poi']+df['shared_receipt_with_poi']

new_features = ['bonus_percent', 'poi_messages']

### Store to my_dataset for easy export below.
df = df.fillna('NaN')
my_dataset = df.T.to_dict()

### Extract features and labels from dataset for local testing
features_list += new_features

data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

##### First, import the necessary packages
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

def create_tune_svm():
    # Creates a pipeline with the SVC, with feature scaling and
    # selection, tunes with GridSearchCV and returns the classifier

    pipe = Pipeline([
        ('scaling', StandardScaler()),
        ('feature_select', SelectKBest()),
        ('svm', SVC())
        ])

    param_grid = [{
        'feature_select__k': [5, 10, 'all'],
        'svm__C': [1, 50, 100, 1000],
        'svm__gamma': [0.5, 0.1, 0.01],
        'svm__kernel': ['linear', 'rbf']
        }]

    clf = GridSearchCV(pipe, cv=3, n_jobs=1, param_grid=param_grid,
    scoring=['precision','recall'], refit='recall').fit(features, labels)

    return clf.best_estimator_

def create_tune_ada():
    # Creates a pipeline with the adaboost classifier with feature
    # selection, tunes with GridSearchCV and returns the classifier

    pipe = Pipeline([
            ('feature_select', SelectKBest()),
            ('ada', AdaBoostClassifier())
            ])

    param_grid = [{
        'feature_select__k': [5, 10, 'all'],
        'ada__n_estimators': [30, 50, 100],
        'ada__learning_rate': [0.5, 0.8, 1]
        }]

    clf = GridSearchCV(pipe, cv=3, n_jobs=1, param_grid=param_grid, 
    scoring=['precision','recall'], refit='recall').fit(features, labels)

    return clf.best_estimator_

def create_tune_kneigh():
    # Creates a pipeline with the K-nearest neighbors classifier with feature
    # selection, tunes with GridSearchCV and returns the classifier

    pipe = Pipeline([
        ('feature_select', SelectKBest()),
        ('kn', KNeighborsClassifier())
        ])

    param_grid = [{
        'feature_select__k': [5, 10, 'all'],
        'kn__n_neighbors': [3, 5, 7, 10],
        'kn__p': [1, 2]
        }]

    clf = GridSearchCV(pipe, cv=3, n_jobs=1, param_grid=param_grid,
    scoring=['precision','recall'], refit='recall').fit(features, labels)

    return clf.best_estimator_



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

### For the final classifier, I decided not to use the engineered features
### since they do not make the cut in the SelectKBest for the best algorithm.

features_list = ['poi', 'salary', 'total_payments', 'bonus', 'deferred_income',
                 'total_stock_value', 'expenses', 'exercised_stock_options', 'other',
                 'long_term_incentive', 'restricted_stock', 'to_messages', 
                 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi',
                 'shared_receipt_with_poi']

data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

clf = Pipeline([
    ('feature_select', SelectKBest(k = 5)),
    ('kn', KNeighborsClassifier(n_neighbors = 3, p = 1))
])

dump_classifier_and_data(clf, my_dataset, features_list)