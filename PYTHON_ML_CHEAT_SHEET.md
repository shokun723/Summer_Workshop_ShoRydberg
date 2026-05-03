# Python and Machine Learning Cheat Sheet

For the Data-driven Decision-making Workshop

This handout is for students who are new to Python. You do not need to memorize these commands. Use this like a dictionary: find the task you want to do, copy the pattern, change the parts marked in plain language, and inspect the result.

## Table of Contents

### Python Basics

[How To Read Python Code](#how-to-read-python-code)

[1. Import Useful Libraries](#import-useful-libraries)

### Working With Data Tables

[2. Load Data Tables](#load-data-tables)

[3. Clean and Inspect Tables](#clean-and-inspect-tables)

[4. Select Data From a Table](#select-data-from-a-table)

[5. Make Basic Plots](#make-basic-plots)

### Regression and Prediction

[6. Prepare Data for Regression](#prepare-data-for-regression)

[7. Train a Regression Model](#train-a-regression-model)

[8. Evaluate Regression](#evaluate-regression)

[9. Polynomial Regression](#polynomial-regression)

### Images as Data

[10. Load Images](#load-images)

[11. Inspect Images](#inspect-images)

[12. Show Images](#show-images)

[13. Convert Image Color](#convert-image-color)

[14. Resize Images](#resize-images)

[15. Split RGB Channels](#split-rgb-channels)

[16. Normalize Pixel Values](#normalize-pixel-values)

[17. Flatten an Image for Classical ML Models](#flatten-an-image-for-classical-ml-models)

[18. SVD Image Compression](#svd-image-compression)

[19. PCA for Image Groups](#pca-for-image-groups)

[20. Add Noise to an Image](#add-noise-to-an-image)

[21. Basic Image Augmentation](#basic-image-augmentation)

### Classification Models

[22. Prepare Labels for Classification](#prepare-labels-for-classification)

[23. Train/Test Split](#traintest-split)

[24. Standardize Features](#standardize-features)

[25. Use a Pipeline](#use-a-pipeline)

[26. Train Common Classification Models](#train-common-classification-models)

[27. Evaluate Classification](#evaluate-classification)

[28. Compare Models](#compare-models)

[29. Inspect Wrong Predictions](#inspect-wrong-predictions)

### Clustering and Defect Localization

[30. Clustering With KMeans](#clustering-with-kmeans)

[31. Build Pixel Features for Clustering](#build-pixel-features-for-clustering)

[32. Defect Localization Settings](#defect-localization-settings)

### Notebook Utilities

[33. Display Markdown Notes in a Notebook](#display-markdown-notes-in-a-notebook)

[34. Time How Long Code Takes](#time-how-long-code-takes)

[35. Save Results to a CSV](#save-results-to-a-csv)

### Student Experiment Guide

[36. Safe Student Change Points](#safe-student-change-points)

[37. The Most Important Questions](#the-most-important-questions)

[38. Mini-Project Template](#mini-project-template)

[39. Beginner Debugging Checklist](#beginner-debugging-checklist)

[40. Tiny Glossary](#tiny-glossary)

## How To Read Python Code

### Comments

Comments start with `#`. Python ignores them. They are notes for humans.

```python
# This is a comment. It explains the code below.
country = "Japan"
```

### Variables

A variable stores a value so you can use it later.

```python
country = "Japan"
year = 2030
image_size = 96
```

You can change the value on the right side.

```python
country = "Mexico"
image_size = 128
```

### Functions

A function does a task. Parentheses hold the inputs.

```python
print("Hello")
len(records)
model.fit(X_train, y_train)
```

### Dots

A dot means "use something that belongs to this object."

```python
gdp.head()
image.resize((100, 100))
model.predict(X_test)
```

Read these as:

- `gdp.head()` means "show the first rows of the dataframe called `gdp`."
- `image.resize(...)` means "resize the image object."
- `model.predict(...)` means "ask the trained model for predictions."

### Common Error Messages

| Error | What it usually means | What to check |
|---|---|---|
| `NameError` | Python does not know that variable name. | Did you run the cell that creates it? Is it spelled the same way? |
| `FileNotFoundError` | Python cannot find the file. | Is the path correct? Is the file in the same folder? |
| `ModuleNotFoundError` | A package is missing. | Did the setup/install step run? |
| `ValueError` | The data has the wrong value or shape. | Check image size, labels, missing values, or class counts. |
| `KeyError` | A column name or dictionary key was not found. | Check spelling and capitalization of the column name. |

## 1. Import Useful Libraries

Use imports at the top of a notebook.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from pathlib import Path
from PIL import Image
```

What they do:

| Command | Purpose |
|---|---|
| `numpy as np` | Work with arrays and numbers. |
| `pandas as pd` | Work with tables/dataframes. |
| `matplotlib.pyplot as plt` | Make plots and show images. |
| `plotly.graph_objects as go` | Make interactive plots such as rotatable 3D scatter plots. |
| `Path` | Work with file and folder paths. |
| `Image` | Open, resize, and convert images. |

## 2. Load Data Tables

### Load a CSV file

```python
data = pd.read_csv("filename.csv")
```

Workshop example:

```python
gdp = pd.read_csv("GDP_Data.csv", delimiter=",", skiprows=4)
```

Change:

- `"GDP_Data.csv"` to your file name.
- `skiprows=4` if your CSV has extra header rows at the top.

Inspect:

```python
data.head()
data.shape
data.columns
data.info()
```

What they show:

| Command | Meaning |
|---|---|
| `data.head()` | First few rows. |
| `data.shape` | Number of rows and columns. |
| `data.columns` | Column names. |
| `data.info()` | Column types and missing values. |

## 3. Clean and Inspect Tables

### Count missing values

```python
data.isna().sum()
```

### Drop empty columns

```python
data_clean = data.dropna(axis="columns", how="all")
```

### Drop rows with missing values

```python
data_clean = data_clean.dropna()
```

### Drop columns you do not need

```python
data_clean = data_clean.drop(columns=["Column A", "Column B"])
```

### Get summary statistics

```python
data.describe()
```

Student warning: cleaning changes the dataset. After cleaning, always inspect:

```python
data_clean.shape
data_clean.head()
data_clean.isna().sum()
```

## 4. Select Data From a Table

### Select one column

```python
data["column_name"]
```

Example:

```python
gdp_transposed["Japan"]
```

### Select several columns

```python
data[["column_1", "column_2"]]
```

### Filter rows using a condition

```python
filtered = data[data["column_name"] == "value"]
```

Example:

```python
clean_records = records[records["damage_status"] == "Not-Damaged"]
```

### Count categories

```python
data["label_column"].value_counts()
```

Example:

```python
records["damage_status"].value_counts()
```

Use this before training a classifier. If one class has many more examples than another, the model may become biased.

## 5. Make Basic Plots

### Line plot

```python
plt.figure(figsize=(8, 5))
plt.plot(x_values, y_values)
plt.xlabel("X label")
plt.ylabel("Y label")
plt.title("Title")
plt.show()
```

### Scatter plot

```python
plt.figure(figsize=(8, 5))
plt.scatter(x_values, y_values)
plt.xlabel("X label")
plt.ylabel("Y label")
plt.show()
```

### Bar plot for class counts

```python
class_counts = records["damage_status"].value_counts()
class_counts.plot(kind="bar")
plt.xlabel("Class")
plt.ylabel("Number of images")
plt.show()
```

### Show a matrix or heatmap

```python
plt.imshow(matrix)
plt.colorbar()
plt.show()
```

Inspect:

- Are there outliers?
- Are classes balanced?
- Does the plot match what you expected?

## 6. Prepare Data for Regression

Regression predicts a number.

Example question: "Can past GDP values help us predict a future GDP value?"

### Make X and y

```python
X = years.reshape(-1, 1)
y = gdp_values
```

Meaning:

| Name | Meaning |
|---|---|
| `X` | Input information the model uses. |
| `y` | Answer the model tries to predict. |

`reshape(-1, 1)` turns a list of numbers into the shape scikit-learn expects.

## 7. Train a Regression Model

### Linear regression

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X, y)
predictions = model.predict(X)
```

What happens:

| Line | Meaning |
|---|---|
| `model = LinearRegression()` | Create the model. |
| `model.fit(X, y)` | Train the model. |
| `model.predict(X)` | Ask the model for predictions. |

### Predict a future value

```python
future_year = np.array([[2030]])
future_prediction = model.predict(future_year)
print(future_prediction)
```

Change:

- `2030` to another year.

Inspect:

- Is the year far outside the training data?
- Does the prediction seem reasonable?
- Are you extrapolating?

## 8. Evaluate Regression

```python
from sklearn.metrics import mean_squared_error, r2_score

rmse = np.sqrt(mean_squared_error(y_true, y_pred))
r2 = r2_score(y_true, y_pred)

print("RMSE:", rmse)
print("R2:", r2)
```

Simple interpretation:

| Metric | Meaning |
|---|---|
| `RMSE` | Average prediction error. Smaller is usually better. |
| `R2` | How much variation the model explains. Closer to 1 is usually better. |

Do not trust a metric by itself. Also inspect the plot.

## 9. Polynomial Regression

Polynomial regression can fit curves.

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

poly_model = make_pipeline(
    PolynomialFeatures(degree=2),
    LinearRegression()
)

poly_model.fit(X, y)
y_pred_poly = poly_model.predict(X)
```

Change:

- `degree=2` to `degree=3` or another number.

Inspect:

- Does the curve fit better?
- Is it becoming too wiggly?
- Would you trust it for future years?

## 10. Load Images

### Load an image from your computer

```python
from PIL import Image

image = Image.open("path/to/image.png")
image
```

Windows path example:

```python
image = Image.open(r"C:\Users\YourName\Pictures\device_image.png")
```

The `r` before the string helps Windows paths work correctly.

### Load an image from a URL

```python
from PIL import Image
from io import BytesIO
import requests

url = "https://example.com/image.jpg"
response = requests.get(url)
image = Image.open(BytesIO(response.content))
image
```

If internet is unreliable, use a local image path instead.

## 11. Inspect Images

```python
print(image.size)
print(image.mode)
```

Meaning:

| Command | Meaning |
|---|---|
| `image.size` | Width and height, like `(1920, 1080)`. |
| `image.mode` | Color mode, such as `RGB` or `L`. |

### Convert image to a NumPy array

```python
image_array = np.array(image)
print(image_array.shape)
print(image_array.dtype)
print(image_array.min(), image_array.max())
```

What to inspect:

| Item | Meaning |
|---|---|
| `shape` | Image dimensions and color channels. |
| `dtype` | Number type, often `uint8` or `float32`. |
| `min`, `max` | Pixel value range. Often 0-255 or 0-1. |

## 12. Show Images

```python
plt.imshow(image)
plt.axis("off")
plt.show()
```

For grayscale:

```python
plt.imshow(gray_image, cmap="gray")
plt.axis("off")
plt.show()
```

## 13. Convert Image Color

### RGB to grayscale

```python
gray_image = image.convert("L")
```

### Grayscale or other mode to RGB

```python
rgb_image = image.convert("RGB")
```

Use RGB when color matters. Use grayscale when shape or brightness matters more than color, or when you want a simpler model.

## 14. Resize Images

```python
resized = image.resize((100, 100))
```

Change:

- `(100, 100)` to another width and height.

Inspect:

```python
print(resized.size)
plt.imshow(resized)
plt.axis("off")
plt.show()
```

Student warning: smaller images run faster, but they may lose tiny defects.

## 15. Split RGB Channels

```python
r, g, b = image.split()
```

Show each channel:

```python
plt.imshow(r, cmap="Reds")
plt.axis("off")
plt.show()
```

Use this when you want to ask: "Is the useful information in color, brightness, or shape?"

## 16. Normalize Pixel Values

Many images start with pixel values from 0 to 255. Normalization changes them to 0 to 1.

```python
image_array = np.array(image).astype("float32")
image_array = image_array / 255.0
```

Inspect:

```python
print(image_array.min(), image_array.max())
```

Expected result: values between 0 and 1.

## 17. Flatten an Image for Classical ML Models

Some models need each image to become one long row of numbers.

```python
flat_image = image_array.flatten()
print(flat_image.shape)
```

Example:

- A `96 x 96` grayscale image becomes `9216` numbers.
- A `96 x 96` RGB image becomes `27648` numbers.

## 18. SVD Image Compression

SVD keeps the strongest patterns in an image.

```python
gray_array = np.array(gray_image, dtype=np.float32)
U, s, Vt = np.linalg.svd(gray_array, full_matrices=False)
```

Rebuild the image using only `k` components:

```python
k = 20
compressed = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]

plt.imshow(compressed, cmap="gray")
plt.axis("off")
plt.show()
```

Change:

- `k = 5`, `20`, `50`, `100`

Inspect:

- When does the image become recognizable?
- What details disappear first?

## 19. PCA for Image Groups

PCA stands for Principal Component Analysis. It helps us take data with many columns and make a smaller view of it.

For images, PCA can help answer: "Do these images naturally form groups before we train a classifier?"

### Basic idea

1. Resize every image to the same size.
2. Convert each image to grayscale or RGB.
3. Flatten each image into one long row of pixel values.
4. Run PCA to reduce each image to 2 or 3 numbers.
5. Plot those numbers as a 2D or 3D scatter plot.

### Run PCA on image rows

```python
from sklearn.decomposition import PCA

PCA_PLOT_DIMENSIONS = 2  # Student change point: try 2 or 3

pca = PCA(n_components=PCA_PLOT_DIMENSIONS, random_state=42)
X_pca_view = pca.fit_transform(X_images)
```

Meaning:

| Command | Meaning |
|---|---|
| `PCA_PLOT_DIMENSIONS = 2` | Make a flat 2D PCA plot. |
| `PCA_PLOT_DIMENSIONS = 3` | Make a 3D PCA plot. |
| `fit_transform(X_images)` | Learn the strongest patterns and transform images into PCA coordinates. |
| `X_pca_view` | A table with 2 or 3 PCA coordinate columns. |

### Plot PCA results in 2D

```python
plt.figure(figsize=(8, 6))
plt.scatter(X_pca_view[:, 0], X_pca_view[:, 1])
plt.xlabel("PCA component 1")
plt.ylabel("PCA component 2")
plt.title("2D PCA view of image groups")
plt.show()
```

If you have labels, color the dots by label:

```python
for label in sorted(set(labels)):
    mask = np.array(labels) == label
    plt.scatter(
        X_pca_view[mask, 0],
        X_pca_view[mask, 1],
        label=label
    )

plt.legend()
plt.show()
```

### Plot PCA results in interactive 3D

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(
    go.Scatter3d(
        x=X_pca_view[:, 0],
        y=X_pca_view[:, 1],
        z=X_pca_view[:, 2],
        mode="markers",
        marker={"size": 6, "opacity": 0.8},
    )
)

fig.update_layout(
    title="Interactive 3D PCA view of image groups",
    scene={
        "xaxis_title": "PCA component 1",
        "yaxis_title": "PCA component 2",
        "zaxis_title": "PCA component 3",
    },
)
fig.show(config={"scrollZoom": True})
```

Drag the Plotly 3D plot to rotate it. Scroll to zoom, and use the modebar tools to pan or reset the view.

Useful Plotly commands:

| Command | Meaning |
|---|---|
| `go.Figure()` | Create an interactive Plotly figure. |
| `go.Scatter3d(...)` | Add 3D scatter points. |
| `mode="markers"` | Draw dots instead of lines. |
| `marker={"size": 6, "opacity": 0.8}` | Control dot size and transparency. |
| `fig.update_layout(scene={...})` | Set 3D axis labels and layout options. |
| `fig.show(config={"scrollZoom": True})` | Show the interactive plot and allow mouse-wheel zoom. |

Inspect:

- Does the 2D or 3D view make the groups easier to see?
- Do images from the same group land near each other?
- Do defect images separate from clean images?
- Could the grouping be caused by lighting, background, or camera angle?
- If the groups overlap, what might make classification harder?

Student warning: PCA is not a classifier. It is a visual preview of structure in the data.

## 20. Add Noise to an Image

```python
noise_level = 60
noise = np.random.normal(0, noise_level, gray_array.shape)
noisy_image = gray_array + noise
```

Keep values in the image range:

```python
noisy_image = np.clip(noisy_image, 0, 255)
```

Change:

- `noise_level`

Inspect:

- Can you still see the important structure?
- Does denoising remove noise or remove useful detail?

## 21. Basic Image Augmentation

Augmentation creates changed copies of images.

Common changes:

```python
flipped = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
rotated = image.rotate(20)
resized = image.resize((224, 224))
```

In the workshop notebooks, augmentation uses helper functions so students do not need to write every image transformation from scratch.

Useful settings to change:

```python
TARGET_CLASS_SIZE = 40
OUTPUT_IMAGE_SIZE = 224
TARGET_MODE = "damage_status"
```

Meaning:

| Setting | Meaning |
|---|---|
| `TARGET_CLASS_SIZE` | How many images each class should have after augmentation. |
| `OUTPUT_IMAGE_SIZE` | Size of exported augmented images. |
| `TARGET_MODE` | What label the model will learn, such as damage status or device type. |

Student warning: augmented images should still look realistic. Bad augmentation can teach the model fake clues.

## 22. Prepare Labels for Classification

Classification predicts a category.

Examples:

- `Damaged` vs `Not-Damaged`
- `device1` vs `device 2`

### Choose the target label

```python
TARGET_MODE = "damage_status"
```

Other possible setting:

```python
TARGET_MODE = "device_type"
```

### Count labels

```python
class_counts = records[target_column].value_counts()
display(class_counts)
```

Inspect:

- Do all classes have enough examples?
- Is one class much larger than another?

## 23. Train/Test Split

Train/test split keeps some data hidden from the model so we can test it more fairly.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    labels,
    test_size=0.30,
    random_state=42,
    stratify=labels
)
```

Meaning:

| Setting | Meaning |
|---|---|
| `test_size=0.30` | 30% of the data is saved for testing. |
| `random_state=42` | Makes the split repeatable. |
| `stratify=labels` | Tries to keep class balance in train and test sets. |

Change:

- `test_size=0.20` or `0.40`
- `random_state=7`, `100`, etc.

Inspect:

- Did the accuracy change?
- Did the mistakes change?

## 24. Standardize Features

Some models work better when features are scaled.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

Important:

- Use `fit_transform` on training data.
- Use `transform` on test data.
- Do not `fit` the scaler on test data.

## 25. Use a Pipeline

A pipeline combines preprocessing and a model.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=2000))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Why pipelines help:

- They keep steps together.
- They reduce mistakes.
- They make testing cleaner.

## 26. Train Common Classification Models

### Logistic Regression

```python
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=2000))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Good first model. Often simple and useful.

### Decision Tree

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Easy to understand, but can overfit.

### K-Nearest Neighbors

```python
from sklearn.neighbors import KNeighborsClassifier

model = Pipeline([
    ("scale", StandardScaler()),
    ("clf", KNeighborsClassifier(n_neighbors=3))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Change:

- `n_neighbors=3` to `5` or `7`

### Linear SVC

```python
from sklearn.svm import LinearSVC

model = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LinearSVC(max_iter=5000, random_state=42))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Useful for high-dimensional data like flattened images.

### Multi-Layer Perceptron

```python
from sklearn.neural_network import MLPClassifier

model = Pipeline([
    ("scale", StandardScaler()),
    ("clf", MLPClassifier(
        hidden_layer_sizes=(128,),
        max_iter=500,
        random_state=42
    ))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Change carefully:

- `hidden_layer_sizes=(128,)`
- `max_iter=500`

## 27. Evaluate Classification

### Accuracy

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)
```

Accuracy means: "What fraction of test examples did the model get right?"

### Classification report

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, predictions))
```

Useful words:

| Word | Simple meaning |
|---|---|
| `precision` | When the model predicts this class, how often is it right? |
| `recall` | Of all real examples of this class, how many did the model find? |
| `f1-score` | A balance of precision and recall. |

### Confusion matrix

```python
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, predictions)
print(cm)
```

Show as an image:

```python
plt.imshow(cm)
plt.colorbar()
plt.xlabel("Predicted label")
plt.ylabel("True label")
plt.show()
```

Inspect:

- Which class is easiest?
- Which classes are confused?
- Which mistake matters most in real life?

## 28. Compare Models

Save model results in a table:

```python
model_summaries = []

model_summaries.append({
    "model": "Logistic Regression",
    "accuracy": accuracy,
    "notes": "Simple baseline"
})

comparison_table = pd.DataFrame(model_summaries)
comparison_table.sort_values(by="accuracy", ascending=False)
```

Choose a model using:

- accuracy
- speed
- type of mistakes
- whether the result is explainable
- whether the model would be trusted outside the workshop dataset

## 29. Inspect Wrong Predictions

After training, do not only look at accuracy. Look at examples the model got wrong.

Pattern:

```python
wrong = y_test != predictions
```

Then inspect images where `wrong` is true.

Questions:

- Does the image look unusual?
- Is the label correct?
- Is lighting, background, blur, or angle confusing the model?
- Did the model learn the device or something around the device?

## 30. Clustering With KMeans

Clustering groups similar data without using labels.

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=3, n_init=10, random_state=42)
cluster_labels = model.fit_predict(features)
```

Meaning:

| Setting | Meaning |
|---|---|
| `n_clusters=3` | Force the data into 3 groups. |
| `n_init=10` | Try multiple starting points. |
| `random_state=42` | Make results reproducible. |

Change:

- `n_clusters=2`, `4`, or `5`

Inspect:

- Do the groups match meaningful regions?
- Or did the model group lighting, shadows, or background?

## 31. Build Pixel Features for Clustering

For image clustering, each pixel can become a row of features.

Example idea:

```python
pixels = image_array.reshape(-1, 3)
```

For RGB images:

- each row is one pixel
- columns are red, green, blue

For grayscale:

```python
pixels = gray_array.reshape(-1, 1)
```

Optional idea: include pixel position so the model knows where each pixel is located.

```python
# Conceptual example
features = np.column_stack([pixel_values, x_positions, y_positions])
```

## 32. Defect Localization Settings

The defect localization notebook has settings students can change.

```python
FOCUS_DEVICE = "device 3"
IMAGE_SIZE = 100
COLOR_MODE = "rgb"
BLUR_RADIUS = 1.0
N_CLUSTERS = 3
USE_POSITION_FEATURES = True
POSITION_WEIGHT = 0.35
ANOMALY_RULE = "deviation_from_clean_reference"
```

Meaning:

| Setting | Meaning |
|---|---|
| `FOCUS_DEVICE` | Which device builds the clean reference. |
| `IMAGE_SIZE` | Smaller is faster; larger may preserve tiny defects. |
| `COLOR_MODE` | Try `"rgb"` or `"grayscale"`. |
| `BLUR_RADIUS` | Smooths noise, but may hide small defects. |
| `N_CLUSTERS` | Number of KMeans groups. |
| `USE_POSITION_FEATURES` | Whether pixel location matters. |
| `POSITION_WEIGHT` | How strongly location matters. |
| `ANOMALY_RULE` | Rule for deciding suspicious regions. |

Inspect:

- Did the highlighted region look like a defect?
- Did it find lighting, edge, shadow, or background instead?

## 33. Display Markdown Notes in a Notebook

The notebooks sometimes display clean text output.

```python
from IPython.display import display, Markdown

display(Markdown("**Important:** inspect the result before moving on."))
```

Useful for making notebooks easier to read.

## 34. Time How Long Code Takes

```python
import time

started = time.perf_counter()

# code to time goes here

elapsed = time.perf_counter() - started
print("Elapsed seconds:", elapsed)
```

Use this when comparing model speed.

## 35. Save Results to a CSV

```python
results.to_csv("results.csv", index=False)
```

Load them later:

```python
results = pd.read_csv("results.csv")
```

## 36. Safe Student Change Points

These are good settings to experiment with.

### Numerical notebook

```python
country_name = "United States"
future_year = np.array([[2030]])
degree = 2
```

Try:

- a different country
- a different future year
- a different polynomial degree

### Image data notebook

```python
local_image_path = None
SVD_IMAGE_MAX_SIDE = 512
k_values = [5, 20, 50, 100]
PCA_PLOT_DIMENSIONS = 2
PCA_IMAGE_SIZE = 48
PCA_COLOR_MODE = "grayscale"
MAX_PCA_IMAGES = 60
noise_level = 60
```

Try:

- a local image path
- smaller/larger resize values
- different SVD `k` values
- different noise levels

### Augmentation notebook

```python
TARGET_MODE = "damage_status"
TARGET_CLASS_SIZE = 40
OUTPUT_IMAGE_SIZE = 224
```

Try:

- `TARGET_MODE = "device_type"`
- `TARGET_CLASS_SIZE = 20` or `60`
- smaller or larger image sizes

### Classification notebooks

```python
TARGET_MODE = "damage_status"
IMAGE_SIZE = 96
TEST_SIZE = 0.30
RANDOM_STATE = 42
CNN_EPOCHS = 6
```

Try:

- `TARGET_MODE = "device_type"`
- `IMAGE_SIZE = 64` or `128`
- `TEST_SIZE = 0.20` or `0.40`
- a different `RANDOM_STATE`

### Clustering notebook

```python
COLOR_MODE = "rgb"
N_CLUSTERS = 3
POSITION_WEIGHT = 0.35
ANOMALY_RULE = "deviation_from_clean_reference"
```

Try:

- `COLOR_MODE = "grayscale"`
- `N_CLUSTERS = 2`, `4`, or `5`
- a smaller or larger `POSITION_WEIGHT`
- a different `ANOMALY_RULE`

## 37. The Most Important Questions

After running any model, ask:

1. What did we change?
2. What happened?
3. Why might that have happened?
4. What did the model get wrong?
5. Would we trust this result outside today's dataset?
6. What decision would we make from this result?
7. What warning would we include with that decision?

## 38. Mini-Project Template

Use this when building your own code or final result.

```python
# 1. Load data
data = pd.read_csv("my_data.csv")

# 2. Inspect data
print(data.shape)
display(data.head())

# 3. Choose input X and answer y
X = data[["column_1", "column_2"]]
y = data["label_column"]

# 4. Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

# 5. Create and train model
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# 6. Predict
predictions = model.predict(X_test)

# 7. Evaluate
print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))
```

For image projects, the main extra step is turning images into arrays before creating `X`.

## 39. Beginner Debugging Checklist

When code breaks:

1. Read the last line of the error message first.
2. Check spelling and capitalization.
3. Run earlier cells in order.
4. Print the variable shape.
5. Print the first few rows with `.head()`.
6. Check file paths.
7. Check for missing values.
8. Try a smaller image size or smaller dataset.
9. Restart the notebook kernel only if variables seem confused.

Useful inspection commands:

```python
print(type(variable))
print(variable.shape)
print(variable[:5])
display(data.head())
```

## 40. Tiny Glossary

| Word | Student-friendly meaning |
|---|---|
| Array | A grid or list of numbers. |
| Dataframe | A table of data. |
| Feature | Input information the model uses. |
| Label | The answer/category the model learns to predict. |
| Model | A simplified pattern learned from data. |
| Train | Let the model learn from examples. |
| Test | Check the model on examples it did not train on. |
| Regression | Predict a number. |
| Classification | Predict a category. |
| Clustering | Group similar things without labels. |
| Accuracy | Fraction of correct predictions. |
| Confusion matrix | Table showing correct and incorrect predictions by class. |
| Overfitting | Model memorizes training data but does not generalize well. |
| Normalization | Put values on a common scale. |
| Augmentation | Create changed copies of images. |
| Pixel | One small part of an image. |
| RGB | Red, green, and blue color channels. |
| Grayscale | Image represented with brightness values only. |
| SVD | A method for separating strong image patterns from weaker details. |
| PCA | A method for turning many image pixels into a smaller number of coordinates for visualization. |

