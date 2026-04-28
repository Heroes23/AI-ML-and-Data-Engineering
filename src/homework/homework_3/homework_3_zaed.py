### Homework #3 1.29.26: 

# Importing Pandas  and Numpy; 
import pandas as pd 
import numpy as np 
from sklearn.tree import DecisionTreeClassifier 

#  File Path; 
file_path = "https://ashfaq-nsclc-dataset.s3.us-east-1.amazonaws.com/ali_datasets/breast-cancer-dataset.csv"

# Read Excel file; 
df = pd.read_csv(file_path)

df.info()
# print(df.head(10)) 
# print(df.columns)

# Data profile
from ydata_profiling import ProfileReport

# Interactive Profile Report 
profile = ProfileReport(df=df, explorative=True)

#Export the profile to a notebook view; 
profile.to_notebook_iframe()

# Lowercasing columns; 
df.columns = df.columns.str.lower()

# Represent age; 
age_stats = df['age'].describe()

min_age = age_stats.loc['min']
q1 = age_stats.loc['25%']
q3 = age_stats.loc['75%']
max_age = age_stats.loc['max']

# Make a copy if you want to keep original ages
# df['age_original'] = df['age']

# Group 1: min → Q1
df.loc[(df['age'] >= min_age) & (df['age'] <= q1), 'age'] = 1

# Group 2: (Q1, Q3]
df.loc[(df['age'] > q1) & (df['age'] <= q3), 'age'] = 2

# Group 3: (Q3, max]
df.loc[(df['age'] > q3) & (df['age'] <= max_age), 'age'] = 3

df['age'].value_counts()

# One Hot Encoding for Categorical Variables

def one_hot_encode(df: pd.DataFrame, columns: list[str] = None, drop_first: bool = False, prefix_sep: str = "_"):
    """
    One-hot encode categorical columns in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list or None, optional
        List of column names to one-hot encode.
        If None, all object/category dtype columns are encoded.
    drop_first : bool, optional
        Whether to drop the first level to avoid multicollinearity.
    prefix_sep : str, optional
        Separator between column name and value in new column names.

    Returns
    -------
    pd.DataFrame
        DataFrame with one-hot encoded columns.
    """
    if columns is None:
        columns = df.select_dtypes(include=["object"]).columns.tolist()

    return pd.get_dummies(df, columns=columns, drop_first=drop_first, prefix_sep=prefix_sep)

columns = [col for col in df.columns.to_list() if col != 'diagnosis result']

print(columns)

features = one_hot_encode(df=df, columns=columns)

features.info()

# Drop the columns with a # symbol
cols_with_pound = [col for col in features.columns.to_list() if '#' in col]

print(cols_with_pound)

updated_cat_columns = [col for col in features.columns.to_list() if col not in cols_with_pound]

# Subset of your categorical DataFrame
features = features[updated_cat_columns]

features.info()

features.columns.to_list()

features.info()

df.head(10)

features.head(10)

age_cols = [col for col in features.columns.to_list() if 'age' in col]

age_cols

## Scikit Learn

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

features['outcome'] = encoder.fit_transform(features['diagnosis result'])

features['outcome'].value_counts()

# Split our data into training and testing sets
from sklearn.model_selection import train_test_split

# DataFrame info
df.info()

features.info()

# Series
features['outcome'].value_counts()

# Numpy Arrays

X = features.drop(labels=['outcome', 'diagnosis result'], axis=1).to_numpy()

y = features['outcome'].to_numpy().reshape(-1, 1)

# Train and Test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, stratify=y)

from sklearn.tree import DecisionTreeClassifier

# Decision Tree
dt = DecisionTreeClassifier(criterion='gini', splitter='best', min_samples_split=3, max_depth=5)

# Fit the training data on the decision tree
dt.fit(X=X_train, y=y_train)

# Predictions
y_pred = dt.predict(X=X_test)

### Model Evaluation:
    # 1. Classification
    #     a. Confusion Matrix
    #     b. Accuracy 
    #     c. F1 Score
    #     d. Precision
    #     e. Recall 
    #     f. Visualizatoin 

from sklearn.metrics import confusion_matrix

# Confusion Matrix
conf_matr = confusion_matrix(y_true=y_test, y_pred=y_pred)

conf_matr

tp, fp = conf_matr[0][0], conf_matr[0][1]
fn, tn = conf_matr[1][0], conf_matr[1][1]

print("True Positive: ", tp)
print("False Positive: ", fp)
print("False Negative", fn)
print("True Negative", tn)

from typing import Union

# Calculate Accuracy
def accuracy(tp: int, tn: int, fp: int, fn: int, as_perc: bool = False) -> Union[float, str]:

    # Summing up the true pos and negative classes
    numerator = tp + tn

    denominator = tp + tn + fp + fn

    # Dividing
    result = round(numerator / denominator, 2)

    if as_perc:
        result = f"{result * 100}%"
    
    return result

acc = accuracy(tp=tp, tn=tn, fp=fp, fn=fn, as_perc=True)

print("Accuracy Score: ", acc)

# Precision, Recall, and F1 Score from scikit-learn
from sklearn.metrics import precision_score, recall_score, f1_score

precision = precision_score(y_true=y_test, y_pred=y_pred)
recall = recall_score(y_true=y_test, y_pred=y_pred)
f1 = f1_score(y_true=y_test, y_pred=y_pred)

print("Precision: ", precision)
print("Recall: ", recall)
print("F1: ", f1)

from sklearn.metrics import accuracy_score

# Get predictions from the X_Train as input
y_train_pred = dt.predict(X=X_train)

# Evaluation on the training set
train_acc = accuracy_score(y_true=y_train, y_pred=y_train_pred)

print("Training Accuracy: ", train_acc)

train_precision = precision_score(y_true=y_train, y_pred=y_train_pred)
train_recall = recall_score(y_true=y_train, y_pred=y_train_pred)
train_f1 = f1_score(y_true=y_train, y_pred=y_train_pred)

print("Train Precision: ", train_precision)
print("Training Recall: ", train_recall)
print("Training F1 Score: ", train_f1)

train_conf_matr = confusion_matrix(y_true=y_train, y_pred=y_train_pred)

train_conf_matr

# Import graphviz and export_graphviz
import graphviz
from sklearn.tree import export_graphviz

# Feature names (all columns except 'outcome' and 'diagnosis result')
feat_names = [col for col in features.columns.to_list() if col not in ['outcome', 'diagnosis result']]

# Import graphviz and export_graphviz
import graphviz
from sklearn.tree import export_graphviz

# Feature names (all columns except 'outcome' and 'diagnosis result')
feat_names = [col for col in features.columns.to_list() if col not in ['outcome', 'diagnosis result']]

# Export to DOT format
dot_data = export_graphviz(
    dt,
    feature_names=feat_names,
    class_names=['Benign', 'Malignant'],
    filled=True,
    rounded=True
)

# Create graphviz object
dot_zaed = graphviz.Source(dot_data)

# Get the image
dot_zaed.render("tree_visual_homework_3_python", format='png', cleanup=True)