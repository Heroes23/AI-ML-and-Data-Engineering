"""
Homework 6: XGBoost vs LightGBM Classification Comparison

Tasks:
1. Review LightGBM.md documentation
2. Find a classification dataset on Kaggle
3. Train XGBoost and LightGBM models
4. Compare accuracy and ROC AUC metrics
5. BONUS: Hyperparameter tuning

Suggested Kaggle datasets:
- Titanic: https://www.kaggle.com/c/titanic
- Breast Cancer: https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data
- Heart Disease: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
- Credit Card Fraud: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_data():
    """
    Load and prepare the dataset.

    For this example, we'll use sklearn's breast cancer dataset.
    Replace this with your Kaggle dataset!

    To use a Kaggle dataset:
    1. Download the dataset from Kaggle
    2. Load it using pandas: pd.read_csv('path/to/your/dataset.csv')
    3. Process and return X, y
    """
    from sklearn.datasets import load_breast_cancer

    # Load dataset
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name='target')

    print("Dataset loaded successfully!")
    print(f"Shape: {X.shape}")
    print(f"Features: {X.columns.tolist()}")
    print(f"Target distribution:\n{y.value_counts()}")
    print(f"Target distribution (%):\n{y.value_counts(normalize=True) * 100}")

    return X, y


def feature_engineering(X, y):
    """
    Perform feature engineering on the dataset.

    This is where you can:
    - Create new features
    - Handle missing values
    - Encode categorical variables
    - Scale/normalize features
    """
    # Make a copy to avoid modifying original
    X_processed = X.copy()

    # Example: Create polynomial features for the first 5 features
    for col in X_processed.columns[:5]:
        X_processed[f'{col}_squared'] = X_processed[col] ** 2

    # Example: Create interaction features
    if len(X_processed.columns) >= 2:
        X_processed['feature_interaction_1'] = X_processed.iloc[:, 0] * X_processed.iloc[:, 1]

    # Scaling features (optional for tree-based models, but can help)
    # Uncomment if you want to scale
    # scaler = StandardScaler()
    # X_processed = pd.DataFrame(
    #     scaler.fit_transform(X_processed),
    #     columns=X_processed.columns
    # )

    print(f"\nFeature engineering complete!")
    print(f"Original features: {X.shape[1]}")
    print(f"New features: {X_processed.shape[1]}")

    return X_processed, y


def train_xgboost_model(X_train, X_val, y_train, y_val):
    """
    Train an XGBoost classifier.
    """
    print("\n" + "="*50)
    print("Training XGBoost Model")
    print("="*50)

    # Create XGBoost classifier
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )

    # Train the model
    xgb_model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=False
    )

    # Make predictions
    y_pred = xgb_model.predict(X_val)
    y_pred_proba = xgb_model.predict_proba(X_val)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_val, y_pred)
    roc_auc = roc_auc_score(y_val, y_pred_proba)

    print(f"\nXGBoost Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC AUC: {roc_auc:.4f}")

    return xgb_model, y_pred, y_pred_proba, accuracy, roc_auc


def train_lightgbm_model(X_train, X_val, y_train, y_val):
    """
    Train a LightGBM classifier.
    """
    print("\n" + "="*50)
    print("Training LightGBM Model")
    print("="*50)

    # Create LightGBM classifier
    lgb_model = lgb.LGBMClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        num_leaves=31,
        random_state=42,
        verbose=-1
    )

    # Train the model
    lgb_model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        callbacks=[lgb.early_stopping(stopping_rounds=10, verbose=False)]
    )

    # Make predictions
    y_pred = lgb_model.predict(X_val)
    y_pred_proba = lgb_model.predict_proba(X_val)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_val, y_pred)
    roc_auc = roc_auc_score(y_val, y_pred_proba)

    print(f"\nLightGBM Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC AUC: {roc_auc:.4f}")

    return lgb_model, y_pred, y_pred_proba, accuracy, roc_auc


def compare_models(xgb_metrics, lgb_metrics):
    """
    Compare XGBoost and LightGBM models.
    """
    print("\n" + "="*50)
    print("Model Comparison")
    print("="*50)

    comparison_df = pd.DataFrame({
        'Model': ['XGBoost', 'LightGBM'],
        'Accuracy': [xgb_metrics['accuracy'], lgb_metrics['accuracy']],
        'ROC AUC': [xgb_metrics['roc_auc'], lgb_metrics['roc_auc']]
    })

    print("\n", comparison_df.to_string(index=False))

    # Determine winner
    print("\n" + "-"*50)
    if xgb_metrics['accuracy'] > lgb_metrics['accuracy']:
        print(f"Accuracy Winner: XGBoost ({xgb_metrics['accuracy']:.4f} > {lgb_metrics['accuracy']:.4f})")
    elif lgb_metrics['accuracy'] > xgb_metrics['accuracy']:
        print(f"Accuracy Winner: LightGBM ({lgb_metrics['accuracy']:.4f} > {xgb_metrics['accuracy']:.4f})")
    else:
        print("Accuracy: Tie")

    if xgb_metrics['roc_auc'] > lgb_metrics['roc_auc']:
        print(f"ROC AUC Winner: XGBoost ({xgb_metrics['roc_auc']:.4f} > {lgb_metrics['roc_auc']:.4f})")
    elif lgb_metrics['roc_auc'] > xgb_metrics['roc_auc']:
        print(f"ROC AUC Winner: LightGBM ({lgb_metrics['roc_auc']:.4f} > {xgb_metrics['roc_auc']:.4f})")
    else:
        print("ROC AUC: Tie")

    return comparison_df


def plot_roc_curves(y_val, xgb_proba, lgb_proba):
    """
    Plot ROC curves for both models.
    """
    plt.figure(figsize=(10, 6))

    # XGBoost ROC curve
    fpr_xgb, tpr_xgb, _ = roc_curve(y_val, xgb_proba)
    xgb_auc = roc_auc_score(y_val, xgb_proba)
    plt.plot(fpr_xgb, tpr_xgb, label=f'XGBoost (AUC = {xgb_auc:.4f})', linewidth=2)

    # LightGBM ROC curve
    fpr_lgb, tpr_lgb, _ = roc_curve(y_val, lgb_proba)
    lgb_auc = roc_auc_score(y_val, lgb_proba)
    plt.plot(fpr_lgb, tpr_lgb, label=f'LightGBM (AUC = {lgb_auc:.4f})', linewidth=2)

    # Diagonal line (random classifier)
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)

    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curve Comparison: XGBoost vs LightGBM', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('roc_curve_comparison.png', dpi=300, bbox_inches='tight')
    print("\nROC curve saved as 'roc_curve_comparison.png'")
    plt.show()


def plot_feature_importance(xgb_model, lgb_model, feature_names):
    """
    Plot feature importance for both models.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # XGBoost feature importance
    xgb_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': xgb_model.feature_importances_
    }).sort_values('importance', ascending=False).head(10)

    axes[0].barh(xgb_importance['feature'], xgb_importance['importance'])
    axes[0].set_xlabel('Importance', fontsize=11)
    axes[0].set_title('XGBoost - Top 10 Feature Importance', fontsize=13, fontweight='bold')
    axes[0].invert_yaxis()

    # LightGBM feature importance
    lgb_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': lgb_model.feature_importances_
    }).sort_values('importance', ascending=False).head(10)

    axes[1].barh(lgb_importance['feature'], lgb_importance['importance'])
    axes[1].set_xlabel('Importance', fontsize=11)
    axes[1].set_title('LightGBM - Top 10 Feature Importance', fontsize=13, fontweight='bold')
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig('feature_importance_comparison.png', dpi=300, bbox_inches='tight')
    print("Feature importance plot saved as 'feature_importance_comparison.png'")
    plt.show()


def hyperparameter_tuning_xgboost(X_train, y_train):
    """
    BONUS: Perform hyperparameter tuning for XGBoost using GridSearchCV.
    """
    print("\n" + "="*50)
    print("BONUS: Hyperparameter Tuning - XGBoost")
    print("="*50)

    # Define parameter grid
    param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1],
        'n_estimators': [50, 100, 200],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0]
    }

    # Create model
    xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss')

    # Grid search
    grid_search = GridSearchCV(
        xgb_model,
        param_grid,
        cv=3,  # 3-fold cross-validation
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )

    print("Starting grid search... This may take a few minutes.")
    grid_search.fit(X_train, y_train)

    print(f"\nBest XGBoost parameters: {grid_search.best_params_}")
    print(f"Best cross-validation ROC AUC: {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_


def hyperparameter_tuning_lightgbm(X_train, y_train):
    """
    BONUS: Perform hyperparameter tuning for LightGBM using GridSearchCV.
    """
    print("\n" + "="*50)
    print("BONUS: Hyperparameter Tuning - LightGBM")
    print("="*50)

    # Define parameter grid
    param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1],
        'n_estimators': [50, 100, 200],
        'num_leaves': [15, 31, 63],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0]
    }

    # Create model
    lgb_model = lgb.LGBMClassifier(random_state=42, verbose=-1)

    # Grid search
    grid_search = GridSearchCV(
        lgb_model,
        param_grid,
        cv=3,  # 3-fold cross-validation
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )

    print("Starting grid search... This may take a few minutes.")
    grid_search.fit(X_train, y_train)

    print(f"\nBest LightGBM parameters: {grid_search.best_params_}")
    print(f"Best cross-validation ROC AUC: {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_


def main():
    """
    Main function to run the entire homework.
    """
    print("="*70)
    print("HOMEWORK 6: XGBoost vs LightGBM Classification")
    print("="*70)

    # Step 1: Load data
    X, y = load_data()

    # Step 2: Feature engineering
    X_processed, y = feature_engineering(X, y)

    # Step 3: Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X_processed, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain set size: {X_train.shape[0]}")
    print(f"Validation set size: {X_val.shape[0]}")

    # Step 4: Train XGBoost
    xgb_model, xgb_pred, xgb_proba, xgb_acc, xgb_auc = train_xgboost_model(
        X_train, X_val, y_train, y_val
    )

    # Step 5: Train LightGBM
    lgb_model, lgb_pred, lgb_proba, lgb_acc, lgb_auc = train_lightgbm_model(
        X_train, X_val, y_train, y_val
    )

    # Step 6: Compare models
    xgb_metrics = {'accuracy': xgb_acc, 'roc_auc': xgb_auc}
    lgb_metrics = {'accuracy': lgb_acc, 'roc_auc': lgb_auc}
    comparison_df = compare_models(xgb_metrics, lgb_metrics)

    # Step 7: Visualizations
    plot_roc_curves(y_val, xgb_proba, lgb_proba)
    plot_feature_importance(xgb_model, lgb_model, X_processed.columns)

    # BONUS: Hyperparameter tuning (uncomment to run)
    # WARNING: This can take several minutes to complete!
    # print("\n" + "="*70)
    # print("BONUS SECTION: Hyperparameter Tuning")
    # print("="*70)
    #
    # best_xgb = hyperparameter_tuning_xgboost(X_train, y_train)
    # best_lgb = hyperparameter_tuning_lightgbm(X_train, y_train)
    #
    # # Evaluate tuned models
    # xgb_tuned_pred = best_xgb.predict(X_val)
    # xgb_tuned_proba = best_xgb.predict_proba(X_val)[:, 1]
    # xgb_tuned_acc = accuracy_score(y_val, xgb_tuned_pred)
    # xgb_tuned_auc = roc_auc_score(y_val, xgb_tuned_proba)
    #
    # lgb_tuned_pred = best_lgb.predict(X_val)
    # lgb_tuned_proba = best_lgb.predict_proba(X_val)[:, 1]
    # lgb_tuned_acc = accuracy_score(y_val, lgb_tuned_pred)
    # lgb_tuned_auc = roc_auc_score(y_val, lgb_tuned_proba)
    #
    # print("\n" + "="*50)
    # print("Tuned Model Results")
    # print("="*50)
    # print(f"\nXGBoost (Tuned):")
    # print(f"  Accuracy: {xgb_tuned_acc:.4f} (Improvement: {xgb_tuned_acc - xgb_acc:+.4f})")
    # print(f"  ROC AUC: {xgb_tuned_auc:.4f} (Improvement: {xgb_tuned_auc - xgb_auc:+.4f})")
    #
    # print(f"\nLightGBM (Tuned):")
    # print(f"  Accuracy: {lgb_tuned_acc:.4f} (Improvement: {lgb_tuned_acc - lgb_acc:+.4f})")
    # print(f"  ROC AUC: {lgb_tuned_auc:.4f} (Improvement: {lgb_tuned_auc - lgb_auc:+.4f})")

    print("\n" + "="*70)
    print("HOMEWORK 6 COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    main()
