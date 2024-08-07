import os
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout, BatchNormalization, Conv2D, MaxPool2D, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image
import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from keras.applications import ResNet152V2
from keras.callbacks import EarlyStopping

# Load and preprocess training data
base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, 'data_cactus_nudum_train2.csv')

# Read the CSV file
data = pd.read_csv(data_path)
print(data.head())
data.reset_index(drop=True, inplace=True)
img_width, img_height = 224, 224

X = []
for i in tqdm(range(data.shape[0])):
    relative_path = data['path'][i]
    path = os.path.join(base_dir, relative_path)
    
    try:
        img = image.load_img(path, target_size=(img_width, img_height))
        img = image.img_to_array(img)
        img = img / 255.0
        X.append(img)
    except FileNotFoundError as e:
        print(f"File not found: {path}")

X = np.array(X)
y = data.drop(['path'], axis=1).to_numpy()

# Ensure data is not empty
if len(X) == 0 or len(y) == 0:
    raise ValueError("No data loaded. Check your file paths and data.")

# Find unique label combinations
unique_labels = {tuple(labels) for labels in y}

# Initialize lists to store indices for each label combination
train_indices = []
validate_indices = []

# Split indices into train and validate sets for each unique label combination
for labels in unique_labels:
    indices = [i for i, label in enumerate(y) if tuple(label) == labels]
    train_idx, validate_idx = train_test_split(indices, random_state=0, test_size=0.1)
    train_indices.extend(train_idx)
    validate_indices.extend(validate_idx)

# Split X and y into train and validate sets based on indices
X_train, X_validate = X[train_indices], X[validate_indices]
y_train, y_validate = y[train_indices], y[validate_indices]
base_dir_test = os.path.dirname(__file__)
data_path_test = os.path.join(base_dir_test, 'data_cactus_nudum_test2.csv')
# Load and preprocess test data
daya_test = pd.read_csv(data_path_test)
Xt = []
for i in tqdm(range(daya_test.shape[0])):
    relative_path = daya_test['path'][i]
    path = os.path.join(base_dir, relative_path)
    
    try:
        img = image.load_img(path, target_size=(img_width, img_height))
        img = image.img_to_array(img)
        img = img / 255.0
        Xt.append(img)
    except FileNotFoundError as e:
        print(f"File not found: {path}")

X_test = np.array(Xt)
y_test = daya_test.drop(['path'], axis=1).to_numpy()

# Define the model
def ResNet152V2_model():
    model = Sequential()
    resnet152v2_base = ResNet152V2(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))

    for layer in resnet152v2_base.layers:
        layer.trainable = False

    model.add(resnet152v2_base)
    model.add(GlobalAveragePooling2D())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(y.shape[1], activation='softmax'))

    return model

model = ResNet152V2_model()
model.summary()

# Compile and fit the model
early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=10, validation_data=(X_validate, y_validate), callbacks=[early_stopping])

with open('modelResnet152_model-1-e100-7-8-24.json', 'w') as f:
    f.write(model.to_json())

model.save("modelResnet152_model-1-e100-7-8-24.h5")
model.save_weights('model_weights-1-e100-7-8-24.h5')