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
