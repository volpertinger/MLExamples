import pandas as pd
import numpy as np
from pandas.core.dtypes.common import is_numeric_dtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

import Settings


class DataSet:
    def __init__(self, path, name):
        self.__path = path
        self.__name = name

    @staticmethod
    def empty():
        return DataSet(None, None)

    def __str__(self):
        return f"path: {self.__path} filename: {self.__name}"

    def path(self):
        return self.__path

    def name(self):
        return self.__name


class MLModel:

    # ------------------------------------------------------------------------------------------------------------------
    # private
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, label):
        self.__is_learned = False
        self.__save_file_path = None
        self.__train_df = None
        self.__label = label
        self.__data_set = DataSet.empty()

    def __check_learn(self):
        return

    def __rf_learn(self):
        pass

    def __svm_learn(self):
        pass

    def __knn_learn(self):
        pass

    def __gbm_learn(self):
        pass

    def __stacking_learn(self):
        pass

    def __after_teach_processing(self):
        self.__is_learned = True
        return

    # TODO: убрать хардкод колонки
    def __before_teach_processing(self, dataset: DataSet):
        self.__data_set = dataset
        self.__train_df = pd.read_csv(self.__data_set.path())
        print("train data info: ")
        self.__train_df.info()
        print(f"data description:\n{self.__train_df.describe()}")

        for column in self.__train_df.columns:
            if is_numeric_dtype(self.__train_df[column]):
                continue
            print(f"converting column {column} to numeric data type")
            self.__train_df[column] = LabelEncoder().fit_transform(self.__train_df[column])

        self.__train_df = self.__train_df.dropna()
        self.__train_df.info()
        X_train = self.__train_df.drop("satisfaction", axis=1)
        Y_train = self.__train_df["satisfaction"]

        logreg = LogisticRegression()
        logreg.fit(X_train, Y_train)
        acc_log = round(logreg.score(X_train, Y_train) * 100, 2)
        print(acc_log)
        return

    # ------------------------------------------------------------------------------------------------------------------
    # public
    # ------------------------------------------------------------------------------------------------------------------

    def teach(self, dataset):
        self.__before_teach_processing(dataset)
        if self.__label == Settings.RF:
            self.__rf_learn()
        elif self.__label == Settings.SVM:
            self.__svm_learn()
        elif self.__label == Settings.KNN:
            self.__knn_learn()
        elif self.__label == Settings.GBM:
            self.__gbm_learn()
        elif self.__label == Settings.STACKING:
            self.__stacking_learn()
        self.__after_teach_processing()
        return

    def is_learned(self):
        self.__check_learn()
        return self.__is_learned

    def label(self):
        return self.__label

    def test(self, test_value):
        return self.__label + test_value
