import pickle
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from os.path import exists

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
        self.__train_df = None  # полный датафрейм для тренировки
        self.__test_df = None  # полный датафрейм для обучения
        self.__predict = None  # вектор предсказанных значений
        self.__test_data = None  # тестовые данные без результата тестирования
        self.__test_result = None  # тестовые данные только с результатом тестирования
        self.__label = label  # название метода обучения
        self.__model = None  # модель машинного обучения
        self.__data_set = DataSet()
        self.check_learn()

    @staticmethod
    def __log(prefix, data):
        print(f"[{prefix}]: {data}")

    @staticmethod
    def __get_separated_data(data):
        main_data = data.drop(Settings.DATASET_RESULT_COLUMN, axis=1)
        result_data = data[Settings.DATASET_RESULT_COLUMN]
        return main_data, result_data

    def __is_save_exists(self):
        save_path = self.__get_save_path(self.__label)
        self.__log("__is_save_exists", f"checking path: {save_path}")
        return exists(save_path)

    def __load_model(self):
        save_path = self.__get_save_path(self.__label)
        self.__log("__load_model", f"loading from path {save_path}")
        self.__model = pickle.load(open(save_path, "rb"))
        return self.__model

    def __save_model(self, model):
        save_path = self.__get_save_path(self.__label)
        self.__log("__save_model", f"saving to path {save_path}")
        pickle.dump(model, open(save_path, "wb"))

    def __teach(self, method, is_stacking=False):
        self.__log("__teach", "start")
        train_data, train_result = self.__get_separated_data(self.__train_df)
        test_data, test_result = self.__get_separated_data(self.__test_df)
        self.__test_data = test_data
        self.__test_result = test_result

        if self.__is_save_exists():
            model = self.__load_model()
        else:
            if is_stacking:
                self.__log("__teach", "stacking")
                estimators = [
                    ('rf', RandomForestClassifier()),
                    ('knn', KNeighborsClassifier()),
                    ('gbm', GradientBoostingClassifier())]
                model = method(estimators=estimators)
            else:
                model = method()
            model.fit(train_data, train_result)
            self.__save_model(model)

        self.__model = model
        acc_log = round(model.score(train_data, train_result) * 100, 2)
        self.__log("__teach", f"acc_log = {acc_log}")
        self.__predict = self.__model.predict(self.__test_data)
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
        return self.__teach(StackingClassifier, True)

    def __after_teach_processing(self):
        self.__is_learned = True
        return

    def __get_train_path(self):
        return self.__data_set.path() + "\\" + Settings.DATASET_TRAIN

    def __get_test_path(self):
        return self.__data_set.path() + "\\" + Settings.DATASET_TRAIN

    def __get_save_path(self, method):
        return self.__data_set.path() + "\\" + method + "_" + Settings.DATASET_SAVE

    def __normalize_df(self, dataframe):
        for column in dataframe:
            if is_numeric_dtype(dataframe[column]):
                continue
            self.__log("__normalize_df", f"converting column {column} to numeric data type")
            dataframe[column] = LabelEncoder().fit_transform(dataframe[column])
        dataframe = dataframe.dropna()
        return dataframe

    def __before_teach_processing(self, dataset: DataSet):
        self.__data_set = dataset
        self.__train_df = pd.read_csv(self.__get_train_path())
        self.__test_df = pd.read_csv(self.__get_test_path())

        self.__train_df = self.__normalize_df(self.__train_df)
        self.__test_df = self.__normalize_df(self.__test_df)
        return

    # ------------------------------------------------------------------------------------------------------------------
    # public
    # ------------------------------------------------------------------------------------------------------------------
    def set_dataset(self, dataset: DataSet):
        self.__data_set = dataset

    def load(self):
        if self.__is_save_exists():
            self.__load_model()
        else:
            return

    def teach(self):
        result = ""
        self.__log("teach", f"teaching dataset {self.__data_set.path()} with method {self.__label}")
        self.__before_teach_processing(self.__data_set)
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
        self.__log("check_learn", f"{self.__label} started")
        result = self.__is_save_exists()
        self.__is_learned = result
        self.load()
        self.__log("check_learn", f"{self.__label} ended, result: {result}")

    def is_learned(self):
        self.check_learn()
        return self.__is_learned

    def label(self):
        return self.__label

    def test(self, test_index):
        try:
            index = int(test_index)
        except ValueError:
            return f"invalid index! Can`t convert to integer"
        if self.__predict is None:
            self.teach()
        max_len = len(self.__predict)
        if max_len <= index:
            return f"invalid index! {index} > {max_len}!"
        if index < 0:
            return f"invalid index! {index} < 0!"
        return f"Predicted data: {self.__predict[index]}\n" \
               f"Test data: {self.__test_result[index]}"
