import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import Settings as Settings
import ML as Saves


def init_demo():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=600)

    demo.show_demo()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

# TODO: отдельная загрузка тестового и учебного дф + имя колонки для тестов

class UI:

    # ------------------------------------------------------------------------------------------------------------------
    # private static
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __init_viewport(label, width, height):
        dpg.create_viewport(title=label, width=width, height=height)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_viewport_vsync(True)

    @staticmethod
    def __init_frame_updater(updater):
        while dpg.is_dearpygui_running():
            updater()
            dpg.render_dearpygui_frame()

    @staticmethod
    def __log(prefix, sender, app_data, user_data):
        print(f"[{prefix}] sender: {sender}, app_data: {app_data}, user_data: {user_data}")

    @staticmethod
    def __log_base(prefix, data):
        print(f"[{prefix}] {data}")

    # ------------------------------------------------------------------------------------------------------------------
    # private
    # ------------------------------------------------------------------------------------------------------------------
    def __init_prime_window(self, tag):
        with dpg.window(tag=tag):
            # Select dataset block
            dpg.add_text(Settings.SELECT_DATASET)
            with dpg.group(horizontal=True):
                with dpg.file_dialog(label=Settings.SELECT_DATASET, width=Settings.FILE_DIALOG_WIDTH,
                                     height=Settings.FILE_DIALOG_HEIGHT, show=False,
                                     callback=self.__callback_select_file):
                    dpg.add_file_extension(".csv", color=(255, 255, 255, 255))
                    dpg.add_file_extension(".*", color=(0, 0, 0, 0))
                # лямбда для показа окна выбора файла
                dpg.add_button(label="Show File Selector", user_data=dpg.last_container(),
                               callback=lambda s, a, u: dpg.configure_item(u, show=True))
                dpg.add_text(tag=Settings.TAG_SELECTED_FILENAME)
            dpg.add_button(label=Settings.CLEAR, callback=self.__callback_clear)
            # Select methods block
            dpg.add_text(Settings.SELECT_ML_METHOD)
            dpg.add_radio_button(Settings.ML_METHODS, callback=self.__callback_change_learn_status)
            # Learn block
            with dpg.group(horizontal=True):
                dpg.add_button(label=Settings.LEARN, callback=self.__callback_learn, width=Settings.BUTTON_WIDTH)
                dpg.add_text("Some test result", tag=Settings.TAG_LEARN_RESULT)
            # Test block
            with dpg.group(horizontal=True):
                dpg.add_button(label=Settings.TEST, width=Settings.BUTTON_WIDTH, callback=self.__callback_test)
                dpg.add_input_text(tag=Settings.TAG_INPUT_TEST_VALUE, width=Settings.INPUT_WIDTH,
                                   hint=Settings.INPUT_TEST_HINT)
            dpg.add_text("", tag=Settings.TAG_TEST_RESULT)
        self.__change_learn_status(self.__current_method.label())
        dpg.set_primary_window(tag, True)

    def __main_updater(self):
        return

    def __get_save_by_label(self, label):
        if label == self.__rf.label():
            return self.__rf
        if label == self.__svm.label():
            return self.__svm
        if label == self.__knn.label():
            return self.__knn
        if label == self.__gbm.label():
            return self.__gbm
        if label == self.__stacking.label():
            return self.__stacking
        return self.__current_method

    def __change_learn_status(self, label):
        self.__current_method = self.__get_save_by_label(label)
        if self.__current_method.is_learned():
            dpg.set_value(Settings.TAG_LEARN_RESULT, Settings.ALREADY_LEARNED)
        else:
            dpg.set_value(Settings.TAG_LEARN_RESULT, Settings.NOT_LEARNED)

    def __change_test_status(self, label):
        self.__current_method = self.__get_save_by_label(label)

    def __clear_test_result(self):
        self.__log_base("__clear_test_result", "clearing test result")
        dpg.set_value(Settings.TAG_TEST_RESULT, "")

    # ------------------------------------------------------------------------------------------------------------------
    # private callbacks
    # ------------------------------------------------------------------------------------------------------------------

    def __callback_change_learn_status(self, sender, app_data, user_data):
        self.__log("__callback_change_learn_status", sender, app_data, user_data)
        self.__clear_test_result()
        self.__change_learn_status(app_data)

    def __callback_learn(self, sender, app_data, user_data):
        self.__log("__callback_learn", sender, app_data, user_data)
        self.__current_method = self.__get_save_by_label(app_data)
        self.__current_method.teach(self.__dataset)
        self.__change_learn_status(app_data)

    def __callback_test(self, sender, app_data, user_data):
        self.__log("__callback_test", sender, app_data, user_data)
        dpg.set_value(Settings.TAG_TEST_RESULT, dpg.get_value(Settings.TAG_INPUT_TEST_VALUE))

    def __callback_select_file(self, sender, app_data, user_data):
        self.__log("__callback_select_file", sender, app_data, user_data)
        self.__dataset = Saves.DataSet(app_data["file_path_name"], app_data["file_name"])
        dpg.set_value(Settings.TAG_SELECTED_FILENAME, app_data["file_name"])
        self.__log_base("__callback_select_file", str(self.__dataset))

    def __callback_clear(self, sender, app_data, user_data):
        self.__log("__callback_clear", sender, app_data, user_data)
        self.__clear_test_result()
        dpg.set_value(Settings.TAG_SELECTED_FILENAME, "")

    # ------------------------------------------------------------------------------------------------------------------
    # public static
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def deactivate():
        dpg.destroy_context()

    @staticmethod
    def init_demo():
        init_demo()

    # ------------------------------------------------------------------------------------------------------------------
    # public
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            width=Settings.VIEWPORT_WIDTH,
            height=Settings.VIEWPORT_HEIGHT,
            label_viewport=Settings.VIEWPORT_LABEL,
            label_prime_window=Settings.PRIME_WINDOW_LABEL
    ):
        self.__prime_window_label = label_viewport
        self.__viewport_label = label_prime_window
        self.__viewport_height = height
        self.__viewport_width = width
        self.__rf = Saves.MLModel(Settings.RF)
        self.__svm = Saves.MLModel(Settings.SVM)
        self.__knn = Saves.MLModel(Settings.KNN)
        self.__gbm = Saves.MLModel(Settings.GBM)
        self.__stacking = Saves.MLModel(Settings.STACKING)
        self.__dataset = Saves.DataSet.empty()
        self.__current_method = self.__rf
        self.__counter = 1
        dpg.create_context()

    def init_gui(self):
        self.__init_prime_window(self.__prime_window_label)
        self.__init_viewport(self.__viewport_label, self.__viewport_width, self.__viewport_height)
        self.__init_frame_updater(self.__main_updater)
