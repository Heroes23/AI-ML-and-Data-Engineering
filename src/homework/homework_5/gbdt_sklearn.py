"""
Gradient Boosted Decision Trees (GBDT) Classification
Using scikit-learn's GradientBoostingClassifier

This script demonstrates GBDT on a classification dataset and
calculates various classification metrics.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report
)
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
import seaborn as sns


def load_dataset():
    """
    Load the Breast Cancer Wisconsin dataset (a common Kaggle dataset).

    This is a binary classification dataset with 569 samples and 30 features.
    Target: 0 = malignant, 1 = benign

    Returns:
    --------
    X : array-like
        Feature matrix
    y : array-like
        Target labels
    feature_names : list
        Names of features
    target_names : list
        Names of target classes
    """
    data = load_breast_cancer()
    X = data.data
    y = data.target
    feature_names = data.feature_names
    target_names = data.target_names

    print("Dataset Information:")
    print(f"Number of samples: {X.shape[0]}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Target classes: {target_names}")
    print(f"Class distribution: {np.bincount(y)}\n")

    return X, y, feature_names, target_names


def train_gbdt_classifier(X_train, y_train, X_test, y_test):
    """
    Train a Gradient Boosted Decision Tree classifier.

    Parameters:
    -----------
    X_train : array-like
        Training features
    y_train : array-like
        Training labels
    X_test : array-like
        Test features
    y_test : array-like
        Test labels

    Returns:
    --------
    model : GradientBoostingClassifier
        Trained GBDT model
    y_pred : array-like
        Predictions on test set
    """
    print("Training Gradient Boosted Decision Tree Classifier...")

    # Initialize GBDT Classifier
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        verbose=0
    )

    # Fit the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    print("Training complete!\n")

    return model, y_pred


def calculate_metrics(y_test, y_pred, target_names):
    """
    Calculate and display classification metrics.

    Parameters:
    -----------
    y_test : array-like
        True labels
    y_pred : array-like
        Predicted labels
    target_names : list
        Names of target classes

    Returns:
    --------
    dict
        Dictionary containing all metrics
    """
    print("=" * 60)
    print("CLASSIFICATION METRICS")
    print("=" * 60)

    # 1. Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n1. Confusion Matrix:")
    print(cm)
    print("\nInterpretation:")
    print(f"   True Negatives (TN): {cm[0, 0]}")
    print(f"   False Positives (FP): {cm[0, 1]}")
    print(f"   False Negatives (FN): {cm[1, 0]}")
    print(f"   True Positives (TP): {cm[1, 1]}")

    # 2. Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n2. Accuracy: {accuracy:.4f}")
    print(f"   ({accuracy * 100:.2f}% of predictions are correct)")

    # 3. Precision
    precision = precision_score(y_test, y_pred, average='binary')
    print(f"\n3. Precision: {precision:.4f}")
    print(f"   (Of all positive predictions, {precision * 100:.2f}% are correct)")

    # 4. Recall (Sensitivity)
    recall = recall_score(y_test, y_pred, average='binary')
    print(f"\n4. Recall: {recall:.4f}")
    print(f"   (Of all actual positives, {recall * 100:.2f}% are detected)")

    # 5. F1 Score
    f1 = f1_score(y_test, y_pred, average='binary')
    print(f"\n5. F1 Score: {f1:.4f}")
    print(f"   (Harmonic mean of precision and recall)")

    print("\n" + "=" * 60)
    print("DETAILED CLASSIFICATION REPORT")
    print("=" * 60)
    print(classification_report(y_test, y_pred, target_names=target_names))

    # Return metrics as dictionary
    metrics = {
        'confusion_matrix': cm,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

    return metrics


def plot_confusion_matrix(cm, target_names):
    """
    Plot the confusion matrix as a heatmap.

    Parameters:
    -----------
    cm : array-like
        Confusion matrix
    target_names : list
        Names of target classes
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=target_names,
        yticklabels=target_names,
        cbar_kws={'label': 'Count'}
    )
    plt.title('Confusion Matrix - GBDT Classifier', fontsize=14, fontweight='bold')
    plt.ylabel('Actual Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig('confusion_matrix_gbdt.png', dpi=300, bbox_inches='tight')
    print("\nConfusion matrix plot saved as 'confusion_matrix_gbdt.png'")


def plot_feature_importance(model, feature_names, top_n=10):
    """
    Plot the top N most important features.

    Parameters:
    -----------
    model : GradientBoostingClassifier
        Trained model
    feature_names : list
        Names of features
    top_n : int
        Number of top features to display
    """
    # Get feature importances
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]

    plt.figure(figsize=(10, 6))
    plt.title(f'Top {top_n} Feature Importances - GBDT Classifier', fontsize=14, fontweight='bold')
    plt.bar(range(top_n), importances[indices], color='steelblue')
    plt.xticks(range(top_n), [feature_names[i] for i in indices], rotation=45, ha='right')
    plt.xlabel('Features', fontsize=12)
    plt.ylabel('Importance', fontsize=12)
    plt.tight_layout()
    plt.savefig('feature_importance_gbdt.png', dpi=300, bbox_inches='tight')
    print("Feature importance plot saved as 'feature_importance_gbdt.png'")


def main():
    """
    Main function to run the GBDT classification pipeline.
    """
    print("=" * 60)
    print("GRADIENT BOOSTED DECISION TREES - CLASSIFICATION")
    print("=" * 60)
    print()

    # 1. Load dataset
    X, y, feature_names, target_names = load_dataset()

    # 2. Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print(f"Training set size: {X_train.shape[0]} samples")
    print(f"Test set size: {X_test.shape[0]} samples\n")

    # 3. Train GBDT classifier
    model, y_pred = train_gbdt_classifier(X_train, y_train, X_test, y_test)

    # 4. Calculate and display metrics
    metrics = calculate_metrics(y_test, y_pred, target_names)

    # 5. Plot confusion matrix
    try:
        plot_confusion_matrix(metrics['confusion_matrix'], target_names)
        plot_feature_importance(model, feature_names)
    except Exception as e:
        print(f"\nNote: Plotting skipped ({e})")

    # 6. Display model parameters
    print("\n" + "=" * 60)
    print("MODEL PARAMETERS")
    print("=" * 60)
    print(f"Number of estimators: {model.n_estimators}")
    print(f"Learning rate: {model.learning_rate}")
    print(f"Max depth: {model.max_depth}")
    print(f"Number of features: {model.n_features_in_}")

    print("\n" + "=" * 60)
    print("HOMEWORK 5 - TASK 2 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
