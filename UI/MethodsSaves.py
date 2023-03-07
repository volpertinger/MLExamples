class MLSave:
    def __init__(self, label):
        self.__is_learned = False
        self.__save_file_path = None
        self.__label = label

    def is_learned(self):
        return self.__is_learned

    def teach(self):
        self.__is_learned = True
        return True

    def label(self):
        return self.__label

    def test(self, test_value):
        return self.__label + test_value


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
