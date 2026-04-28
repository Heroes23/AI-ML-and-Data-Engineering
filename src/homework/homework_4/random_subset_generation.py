import pandas as pd
import numpy as np


def generate_random_subset(df, n_features=None, random_state=None):
    """
    Generate a random subset of a DataFrame for Random Forest training.

    This function implements bootstrap sampling (sampling with replacement) for rows
    and random feature selection for columns, which are core techniques in Random Forests.

    Parameters:
    -----------
    df : pandas.DataFrame
        The training dataset to sample from
    n_features : int, optional
        Number of features to randomly select. If None, uses sqrt(total_features)
        as commonly done in Random Forests for classification
    random_state : int, optional
        Random seed for reproducibility

    Returns:
    --------
    pandas.DataFrame
        A random subset with:
        - Same number of rows as input (sampled with replacement)
        - A random subset of n_features columns

    Example:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8], 'C': [9, 10, 11, 12]})
    >>> subset = generate_random_subset(df, n_features=2, random_state=42)
    >>> print(subset.shape)
    (4, 2)  # Same number of rows, 2 random features
    """
    if random_state is not None:
        np.random.seed(random_state)

    n_samples = len(df)
    n_total_features = len(df.columns)

    # If n_features not specified, use sqrt of total features (common for classification)
    if n_features is None:
        n_features = int(np.sqrt(n_total_features))
        # Ensure at least 1 feature is selected
        n_features = max(1, n_features)

    # Ensure n_features doesn't exceed total available features
    n_features = min(n_features, n_total_features)

    # Step 1: Bootstrap sampling - sample rows WITH replacement
    # This allows the same row to appear multiple times
    sampled_indices = np.random.choice(n_samples, size=n_samples, replace=True)
    bootstrapped_df = df.iloc[sampled_indices].reset_index(drop=True)

    # Step 2: Random feature selection - select random subset of columns WITHOUT replacement
    selected_features = np.random.choice(df.columns, size=n_features, replace=False)

    # Step 3: Return the subset with selected rows and features
    random_subset = bootstrapped_df[selected_features]

    return random_subset


# Example usage and testing
if __name__ == "__main__":
    # Create a sample DataFrame
    sample_data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [10, 20, 30, 40, 50],
        'feature3': [100, 200, 300, 400, 500],
        'feature4': [5, 10, 15, 20, 25],
        'target': [0, 1, 0, 1, 0]
    })

    print("Original DataFrame:")
    print(sample_data)
    print(f"\nShape: {sample_data.shape}")

    # Generate random subset
    subset = generate_random_subset(sample_data, n_features=3, random_state=42)

    print("\n" + "="*50)
    print("Random Subset (Bootstrap + Feature Selection):")
    print(subset)
    print(f"\nShape: {subset.shape}")
    print(f"Selected features: {list(subset.columns)}")

    # Demonstrate that rows can repeat (bootstrap sampling)
    print("\n" + "="*50)
    print("Note: Some rows may appear multiple times due to sampling with replacement")
