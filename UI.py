import ML

import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import Settings as Settings


def init_demo():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=600)
    demo.show_demo()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


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
                                     height=Settings.FILE_DIALOG_HEIGHT, show=False, directory_selector=True,
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
                dpg.add_button(label=Settings.LEARN, callback=self.__callback_learn, width=Settings.BUTTON_WIDTH,
                               enabled=False, tag=Settings.TAG_LEARN_BUTTON)
                dpg.add_text("Some test result", tag=Settings.TAG_LEARN_RESULT)
            # Test block
            with dpg.group(horizontal=True):
                dpg.add_button(label=Settings.TEST, width=Settings.BUTTON_WIDTH, callback=self.__callback_test,
                               enabled=False, tag=Settings.TAG_TEST_BUTTON)
                dpg.add_input_text(tag=Settings.TAG_INPUT_TEST_VALUE, width=Settings.INPUT_WIDTH,
                                   hint=Settings.INPUT_TEST_HINT, enabled=False)
            dpg.add_text("", tag=Settings.TAG_TEST_RESULT)
            # Loading
            dpg.add_loading_indicator(circle_count=8, show=False, tag=Settings.TAG_LOADING)
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
            self.__enable_test_block()
        else:
            dpg.set_value(Settings.TAG_LEARN_RESULT, Settings.NOT_LEARNED)
            self.__disable_test_block()

    def __change_test_status(self, label):
        self.__current_method = self.__get_save_by_label(label)

    def __clear_test_result(self):
        self.__log_base("__clear_test_result", "clearing test result")
        dpg.set_value(Settings.TAG_TEST_RESULT, "")

    def __dataset_change_processing(self):
        self.__rf.set_dataset(self.__dataset)
        self.__svm.set_dataset(self.__dataset)
        self.__knn.set_dataset(self.__dataset)
        self.__gbm.set_dataset(self.__dataset)
        self.__stacking.set_dataset(self.__dataset)
        self.__change_learn_status(self.__current_method.label())

    @staticmethod
    def __disable_test_block():
        dpg.disable_item(Settings.TAG_TEST_BUTTON)
        dpg.disable_item(Settings.TAG_INPUT_TEST_VALUE)
        dpg.set_value(Settings.TAG_INPUT_TEST_VALUE, "")

    @staticmethod
    def __enable_test_block():
        dpg.enable_item(Settings.TAG_TEST_BUTTON)
        dpg.enable_item(Settings.TAG_INPUT_TEST_VALUE)

    def __enable_ml(self):
        dpg.enable_item(Settings.TAG_LEARN_BUTTON)
        self.__enable_test_block()

    def __disable_ml(self):
        dpg.disable_item(Settings.TAG_LEARN_BUTTON)
        self.__disable_test_block()

    @staticmethod
    def __disable_load():
        dpg.hide_item(Settings.TAG_LOADING)

    @staticmethod
    def __enable_load():
        dpg.show_item(Settings.TAG_LOADING)

    # ------------------------------------------------------------------------------------------------------------------
    # private callbacks
    # ------------------------------------------------------------------------------------------------------------------

    def __callback_change_learn_status(self, sender, app_data, user_data):
        self.__enable_load()
        self.__log("__callback_change_learn_status", sender, app_data, user_data)
        self.__clear_test_result()
        self.__current_method.load()
        self.__change_learn_status(app_data)
        self.__disable_load()

    def __callback_learn(self, sender, app_data, user_data):
        self.__enable_load()
        self.__log("__callback_learn", sender, app_data, user_data)
        self.__current_method = self.__get_save_by_label(app_data)
        self.__current_method.teach()
        self.__change_learn_status(app_data)
        self.__disable_load()

    def __callback_test(self, sender, app_data, user_data):
        self.__enable_load()
        self.__current_method.load()
        self.__log("__callback_test", sender, app_data, user_data)
        dpg.set_value(Settings.TAG_TEST_RESULT,
                      self.__current_method.test(dpg.get_value(Settings.TAG_INPUT_TEST_VALUE)))
        self.__disable_load()

    def __callback_select_file(self, sender, app_data, user_data):
        self.__log("__callback_select_file", sender, app_data, user_data)
        self.__dataset = ML.DataSet(app_data["file_path_name"])
        self.__dataset_change_processing()
        self.__enable_ml()
        self.__callback_change_learn_status(sender, app_data, user_data)
        dpg.set_value(Settings.TAG_SELECTED_FILENAME, self.__dataset.name())
        self.__log_base("__callback_select_file", str(self.__dataset))

    def __callback_clear(self, sender, app_data, user_data):
        self.__log("__callback_clear", sender, app_data, user_data)
        self.__clear_test_result()
        self.__dataset = ML.DataSet()
        self.__dataset_change_processing()
        self.__disable_ml()
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
        self.__rf = ML.MLModel(Settings.RF)
        self.__svm = ML.MLModel(Settings.SVM)
        self.__knn = ML.MLModel(Settings.KNN)
        self.__gbm = ML.MLModel(Settings.GBM)
        self.__stacking = ML.MLModel(Settings.STACKING)
        self.__dataset = ML.DataSet()
        self.__current_method = self.__rf
        self.__counter = 1
        dpg.create_context()

    def init_gui(self):
        self.__init_prime_window(self.__prime_window_label)
        self.__init_viewport(self.__viewport_label, self.__viewport_width, self.__viewport_height)
        self.__init_frame_updater(self.__main_updater)
