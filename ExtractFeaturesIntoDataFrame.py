import cv2 as cv
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sys import platform
from FeatureExtraction.feature_set_a import get_statistics, get_feature_names


MAC_PICTURES_PATH = '/Users/victorhe/Pictures/'
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures\\TrainingBatches\\three'


def images_to_data_frame(batch_name):
    feature_matrix = extract_feature_matrix(batch_name)

    labels_vector = read_labels_into_vector(batch_name)

    data = np.hstack((feature_matrix, labels_vector))

    columns = get_feature_names()
    columns.append('Labels')
    df = pd.DataFrame(data, columns=columns)

    pickle_file_name = batch_name + '.pickle'
    pickle_file_name = get_base_path(batch_name) / pickle_file_name
    with open(pickle_file_name, 'wb') as f:
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)


def extract_feature_matrix(batch_name):
    image_paths = sorted(get_base_path(batch_name).glob('*.BMP'))
    feature_vectors = list()
    for path in image_paths:
        image = cv.imread(str(path))
        roi = get_roi(image)
        converted_image = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        feature_vectors.append(get_statistics(converted_image))
    feature_matrix = np.vstack(feature_vectors)
    return feature_matrix


def get_roi(image):
    # [start_row:end_row, start_col:end_col]
    roi = image[60:940, 260:1140]
    return roi


def read_labels_into_vector(batch_name):
    labels_path = get_base_path(batch_name) / 'labels.txt'
    labels_vector = None
    with open(labels_path) as labels_file:
        for line in labels_file:
            labels_from_file = line.split()
            # converts any label besides '1' and '2' to '5'
            labels_from_file = list(map(lambda x: '5' if x > '2' else x, labels_from_file))
            labels_vector = np.array(labels_from_file).reshape((-1, 1))
    return labels_vector


def get_base_path(batch_name):
    base_path = MAC_PICTURES_PATH if platform == "darwin" else WINDOWS_PICTURES_PATH
    return Path(base_path) / batch_name


def load_data_frame_from_pickle(batch_name):
    pickle_file_name = batch_name + '.pickle'
    pickle_file_name = get_base_path(batch_name) / pickle_file_name
    with open(pickle_file_name, 'rb') as f:
        df = pickle.load(f)
    return df


def concatenate_data_frames(frames, batch_name):
    df = pd.concat(frames, ignore_index=True)
    pickle_file_name = batch_name + '.pickle'
    pickle_file_name = get_base_path(batch_name)/ pickle_file_name
    with open(pickle_file_name, 'wb') as f:
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)


# images_to_data_frame('batch_test')
'''
batch_test_df = load_data_frame_from_pickle('batch_test')
one_df = batch_test_df.loc[batch_test_df['Labels'] == '1']
five_df = batch_test_df.loc[batch_test_df['Labels'] == '5']
sample_size = min(len(one_df), len(five_df))
df_s = [one_df[:sample_size], five_df[:sample_size]]
res = pd.concat(df_s, ignore_index=True)
print(res)
'''
# data, labels = batch_test_df.iloc[:, :6], batch_test_df.iloc[:, 6]

# batch_9_df = load_data_frame_from_pickle('batch_9')
# batch_10_df = load_data_frame_from_pickle('batch_10')
# batch_11_df = load_data_frame_from_pickle('batch_11')

# concatenate_data_frames([batch_9_df, batch_10_df, batch_11_df], 'batch_b')
# batch_b_df = load_data_frame_from_pickle('batch_b')
# print(batch_b_df['Labels'].value_counts())