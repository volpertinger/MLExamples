# ----------------------------------------------------------------------------------------------------------------------
# Viewport
# ----------------------------------------------------------------------------------------------------------------------
VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 500
VIEWPORT_LABEL = "ML Viewport"

# ----------------------------------------------------------------------------------------------------------------------
# Prime window
# ----------------------------------------------------------------------------------------------------------------------
PRIME_WINDOW_LABEL = "ML prime window"

# ----------------------------------------------------------------------------------------------------------------------
# Methods
# ----------------------------------------------------------------------------------------------------------------------
RF = "RF"
SVM = "SVM"
KNN = "kNN"
GBM = "GBM"
STACKING = "Stacking"

# ----------------------------------------------------------------------------------------------------------------------
# Selectables
# ----------------------------------------------------------------------------------------------------------------------
ML_METHODS = [RF, SVM, KNN, GBM, STACKING]

# ----------------------------------------------------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------------------------------------------------
INPUT_WIDTH = 200
INPUT_TEST_HINT = "Enter test index for check"

# ----------------------------------------------------------------------------------------------------------------------
# Buttons
# ----------------------------------------------------------------------------------------------------------------------
LEARN = "Teach"
TEST = "Test"
CLEAR = "Clear"
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50

# ----------------------------------------------------------------------------------------------------------------------
# File dialogs
# ----------------------------------------------------------------------------------------------------------------------
FILE_DIALOG_WIDTH = 500
FILE_DIALOG_HEIGHT = 400

# ----------------------------------------------------------------------------------------------------------------------
# Tags
# ----------------------------------------------------------------------------------------------------------------------
TAG_LEARN_RESULT = "LearnResultLabel"
TAG_TEST_RESULT = "TestResultLabel"
TAG_INPUT_TEST_VALUE = "InputTest"
TAG_SELECTED_FILENAME = "SelectedFile"
TAG_ERRORS = "Errors"

# ----------------------------------------------------------------------------------------------------------------------
# Datasets
# ----------------------------------------------------------------------------------------------------------------------
DATASET_EXT = ".csv"
DATASET_TRAIN = "train" + DATASET_EXT
DATASET_TEST = "test" + DATASET_EXT
DATASET_SAVE = "save"
# TODO: убрать хардкод колонки
DATASET_RESULT_COLUMN = "satisfaction"

# ----------------------------------------------------------------------------------------------------------------------
# Other
# ----------------------------------------------------------------------------------------------------------------------
ALREADY_LEARNED = "Learned successfully"
NOT_LEARNED = "Not learned"
SELECT_ML_METHOD = "Select ML method"
SELECT_DATASET = "Select dataset"
SELECT_ACTION = "Select action"
INPUT_VALUE_FOR_TEST = "Input value for test"
