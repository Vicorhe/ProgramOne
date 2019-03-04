import tensorflow as tf
from Datasets.utils import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from FeatureExtraction.feature_set_b import get_statistics, FEATURE_VECTOR_SIZE


# load data set
x_train, y_train, x_test, y_test = load_tile_data_set(feature_func=get_statistics)


model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(32, activation=tf.nn.relu, input_shape=[FEATURE_VECTOR_SIZE]),
    tf.keras.layers.Dense(3, activation=tf.nn.softmax)
])


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=8)

model.evaluate(x_test, y_test)