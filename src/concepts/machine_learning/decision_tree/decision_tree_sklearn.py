import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz

# Decision Tree
dt = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=3)

# Usage
X = np.array([
    [2,3],
    [1,1],
    [3,4],
    [5,2],
    [4,2]
])

y = np.array([0,0,0,1,1])

dt.fit(X, y)

X_test = [[3,2], [1,2]]

y_pred = dt.predict(X_test)

print(y_pred)

# Feature names
feat_names = ['feat1', 'feat2']

# Export to DOT format (correct way)
dot_data = export_graphviz(
    dt, 
    feature_names=feat_names,
    class_names=['Class_0', 'Class_1'],
    filled=True,
    rounded=True
)

# Create graphviz object
dot_zaed = graphviz.Source(dot_data)

# Get the image
dot_zaed.render("tree_visual_zaed", format='png', cleanup=True)