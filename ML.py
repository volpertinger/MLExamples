import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from os.path import exists
import pickle

import Settings


class DataSet:
    def __init__(self, path: str = ""):
        self.__path = path
        self.__name = path.split("\\")[-1]

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
        self.__data_set = DataSet()

    @staticmethod
    def __log(prefix, data):
        print(f"[{prefix}]: {data}")

    def __get_train_data(self):
        train_data = self.__train_df.drop(Settings.DATASET_RESULT_COLUMN, axis=1)
        train_result = self.__train_df[Settings.DATASET_RESULT_COLUMN]
        return train_data, train_result

    def __is_save_exists(self):
        save_path = self.__get_save_path(self.__label)
        return exists(save_path)

    def __load_model(self):
        save_path = self.__get_save_path(self.__label)
        self.__log("__load_model", f"loading from path {save_path}")
        return pickle.load(open(save_path, "rb"))

    def __save_model(self, model):
        save_path = self.__get_save_path(self.__label)
        self.__log("__save_model", f"saving to path {save_path}")
        pickle.dump(model, open(save_path, "wb"))

    def __teach(self, method):
        train_data, train_result = self.__get_train_data()

        if self.__is_save_exists():
            model = self.__load_model()
        else:
            model = method()
            model.fit(train_data, train_result)
            self.__save_model(model)

        acc_log = round(model.score(train_data, train_result) * 100, 2)
        self.__log("__teach", f"acc_log = {acc_log}")
        return acc_log

    def __rf_learn(self):
        return self.__teach(RandomForestClassifier)

    def __svm_learn(self):
        return self.__teach(LinearSVC)

    def __knn_learn(self):
        return self.__teach(KNeighborsClassifier)

    def __gbm_learn(self):
        return self.__teach(GradientBoostingClassifier)

    def __stacking_learn(self):
        pass

    def __after_teach_processing(self):
        self.__is_learned = True
        return

    def __get_train_path(self):
        return self.__data_set.path() + "\\" + Settings.DATASET_TRAIN

    def __get_save_path(self, method):
        return self.__data_set.path() + "\\" + method + "_" + Settings.DATASET_SAVE

    def __before_teach_processing(self, dataset: DataSet):
        self.__data_set = dataset
        self.__train_df = pd.read_csv(self.__get_train_path())

        for column in self.__train_df.columns:
            if is_numeric_dtype(self.__train_df[column]):
                continue
            print(f"converting column {column} to numeric data type")
            self.__train_df[column] = LabelEncoder().fit_transform(self.__train_df[column])

        self.__train_df = self.__train_df.dropna()
        return

    # ------------------------------------------------------------------------------------------------------------------
    # public
    # ------------------------------------------------------------------------------------------------------------------

    def teach(self, dataset):
        result = ""
        self.__log("teach", f"teaching dataset {dataset.path()} with method {self.__label}")
        self.__before_teach_processing(dataset)
        if self.__label == Settings.RF:
            result = self.__rf_learn()
        elif self.__label == Settings.SVM:
            result = self.__svm_learn()
        elif self.__label == Settings.KNN:
            result = self.__knn_learn()
        elif self.__label == Settings.GBM:
            result = self.__gbm_learn()
        elif self.__label == Settings.STACKING:
            result = self.__stacking_learn()
        print(result)
        self.__after_teach_processing()
        return

    def check_learn(self):
        self.__is_learned = self.__is_save_exists()

    def is_learned(self):
        self.check_learn()
        return self.__is_learned

    def label(self):
        return self.__label

    def test(self, test_value):
        return self.__label + test_value
