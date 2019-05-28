"""
Operations used to modify the Training DataFrame
"""
import pandas as pd


def ignore_label(label, df):
    return df.loc[df['Labels'] != label]


def make_label_ratio_equal(df):
    unique_labels = df.Labels.unique()
    sample_size = min(df['Labels'].value_counts())
    df_s = [df_with_label(label, df, sample_size) for label in unique_labels]
    return pd.concat(df_s, ignore_index=True)


def df_with_label(label, df, size=None):
    """
    Extracts a DataFrame with set label and sample size (if provided).
    """
    df = df.loc[df['Labels'] == label]
    if size:
        return df[:size]
    else:
        return df


def shuffle_data_set(df):
    return df.sample(frac=1).reset_index(drop=True)


def print_labels_distribution(df):
    print('\nLabels Distribution:\n', df['Labels'].value_counts(), sep='', end='\n\n')


def custom(df):
    label = '5'
    a = ignore_label(label, df)
    a = make_label_ratio_equal(a)
    b = df_with_label(label, df)
    return pd.concat([a, b], ignore_index=True)
