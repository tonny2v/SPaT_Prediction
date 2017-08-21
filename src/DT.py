# Copyright 2017 Priscilla Boyd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""The DT class:

Implements the CART algorithm for decision trees

"""
import os

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, export_graphviz
import matplotlib.pyplot as plt


# returns the latest dataset location
def get_latest_dataset_folder():
    folder = '../results/'
    latest_location = max([os.path.join(folder, d) for d in os.listdir(folder)])
    return latest_location


# returns the latest dataset
def get_latest_dataset():
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset.csv'
    return file


# get X and y for sklearn models, excluding date/time stamps
def get_sklearn_data():
    file = get_latest_dataset()
    data = pd.read_csv(file, usecols=['Phase', 'Result', 'Duration'], sep=',')
    X = data.drop('Duration', axis=1)
    y = data.Duration
    print("Dataset used: ", file)
    return X, y


# implement CART
def run_CART():
    # declare X and y
    X, y = get_sklearn_data()

    # split data into training / test (20% for test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # create decision tree model
    dt_model = DecisionTreeRegressor(max_depth=4)
    # rf_model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1)

    # fit model using training data
    dt_model.fit(X_train, y_train)
    dt_model.predict(X_test)

    # expose to tree graphviz format for analysis
    folder = get_latest_dataset_folder()
    out_file_location = folder + "/dt_tree.dot"
    export_graphviz(dt_model, out_file=out_file_location, feature_names=X_train.columns)

    # predict on new (test) data and encapsulate result in data frame
    y_prediction = dt_model.predict(X_test)

    # get the coefficient of determination to measure how good the random forest model is
    score = dt_model.score(X_test, y_test)
    print("Total score:", score)

    # plot for visualisation
    plt.scatter(y_prediction, y_test, label='Duration')
    plt.plot([0, 1], [0, 1], '--k', transform=plt.gca().transAxes)
    plt.xlabel('y_prediction')
    plt.ylabel('y_test')
    plt.show()


# main function runs data processing for decision trees
if __name__ == '__main__':
    run_CART()
