# Workshop Week Plan

## Workshop Goal

Students should leave the week less intimidated by machine learning tools and more comfortable asking practical questions with data. The emphasis is hands-on exploration, visual interpretation, and decision-making, not deep theory.

## Guiding Story

From device to data to decision:

1. We fabricate devices.
2. We collect data about them.
3. We prepare the data so a computer can use it.
4. We train or run models.
5. We inspect the model's behavior.
6. We decide what the result is useful for, and what it cannot prove.

## Topic 1: Numerical Data and Prediction

Notebook: `0_Class_Notebooks/01_Know_Data_Numerical.ipynb`

Main ideas:

- Data tables, columns, missing values, and plots.
- Regression as a fitted trend.
- Prediction versus extrapolation.
- Why model outputs need judgment.

Student decisions:

- Pick countries or regions to compare.
- Change the training years.
- Decide whether a future prediction seems trustworthy.

Exit question:

What is one situation where the model was helpful, and one situation where you would not trust it?

## Topic 2: Images Are Data

Notebook: `0_Class_Notebooks/02_Know_Data_Images.ipynb`

Optional bridge: `0_Class_Notebooks/02B_Optional_Know_Data_Images_Fourier.ipynb`

Main ideas:

- Images are arrays of numbers.
- Color, grayscale, resizing, scaling, and normalization change what the model sees.
- Compression and SVD show that images contain both important structure and removable detail.
- Augmentation creates new training examples from existing images.
- Fourier views show images as low-frequency broad structure and high-frequency fine detail.

Student decisions:

- Decide when resizing destroys useful information.
- Compare RGB and grayscale versions.
- Identify which image differences are caused by the device and which are caused by lighting, angle, or background.

Exit question:

What image preparation choice might accidentally make a model worse?

Optional Fourier exit question:

Which details in a device image seem more like low-frequency structure, and which seem more like high-frequency texture, edges, or defects?

## Topic 3: Classification

Notebooks:

- `0_Class_Notebooks/03_Image_Augmentation_Workbench.ipynb`
- `0_Class_Notebooks/04_Image_Classification_Grayscale.ipynb`
- `0_Class_Notebooks/05_Image_Classification_RGB.ipynb`

Main ideas:

- Supervised learning uses labeled examples.
- Train/test split gives the model a fairer check.
- Accuracy is useful but incomplete.
- Mistakes often reveal what the model is actually noticing.

Student decisions:

- Predict which model will perform best before running it.
- Compare grayscale and RGB results.
- Inspect misclassified images.
- Decide whether accuracy, speed, or interpretability matters most.

Exit question:

Which model would your group choose today, and what evidence supports that choice?

## Topic 4: Clustering and Defect Localization

Notebook: `0_Class_Notebooks/06_Defect_Localization_Clustering.ipynb`

Main ideas:

- Unsupervised learning can group data without labels.
- Clustering may find useful structure, but it may also find lighting, shadows, or background artifacts.
- Defect localization can be treated as a comparison problem: what looks different from a clean reference?

Student decisions:

- Guess natural groups before running clustering.
- Compare human grouping with machine grouping.
- Adjust parameters and observe how the result changes.
- Decide whether highlighted regions look like true defects.

Exit question:

Did the model find device defects, or did it find something else in the image?

## Topic 5: Mini-Project and Decision Day

Notebook: `0_Class_Notebooks/07_Student_ML_Experiment_Log.ipynb`

Group project choices:

- Can we classify device type from images?
- Can we classify damaged versus not damaged?
- Does RGB perform better than grayscale?
- Does augmentation improve classification?
- Can clustering point to likely defect regions?
- Which model is best if we care about both accuracy and speed?
- Which errors would matter most in a real inspection workflow?

Final group deliverable:

- One question.
- One dataset or image group.
- One model or method.
- One plot or table.
- One correct or useful result.
- One mistake, failure, or limitation.
- One recommendation.

## Note to Self

For this audience, the most important teaching move is to pause at decision points. Students do not need to understand every line of code. They should understand what was changed, what happened, and whether the result supports a decision.

Useful repeated prompt:

What did we change? What happened? Why might that have happened? Would we trust this result outside today's dataset?
