import sys
import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import make_pipeline
import itertools

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t')

for (n_estimators, max_depth,
     max_features, criterion,
     min_weight_fraction_leaf) in itertools.product([500],
                                                    [None],
                                                    [0.1, 0.25, 0.5, 0.75, 'sqrt', 'log2', None],
                                                    ['gini'],
                                                    np.arange(0., 1.01, 0.05)):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(StandardScaler(),
                            RandomForestClassifier(n_estimators=n_estimators,
                                                   max_depth=max_depth,
                                                   max_features=max_features,
                                                   criterion=criterion,
                                                   min_weight_fraction_leaf=min_weight_fraction_leaf))
                                                   
        # 10-fold CV scores for the pipeline
        cv_scores = cross_val_score(estimator=clf, X=features, y=labels, cv=10)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'n_estimators={},'.format(n_estimators)
    param_string += 'max_depth={},'.format(max_depth)
    param_string += 'max_features={},'.format(max_features)
    param_string += 'criterion={},'.format(criterion)
    param_string += 'min_weight_fraction_leaf={}'.format(min_weight_fraction_leaf)

    for cv_score in cv_scores:
        out_text = '\t'.join([dataset.split('/')[-1][:-7],
                              'RandomForestClassifier',
                              param_string,
                              str(cv_score)])

        print(out_text)
        sys.stdout.flush()