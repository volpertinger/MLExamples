import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import UI.Settings as Settings
import UI.MethodsSaves as Saves


def init_demo():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=600)

    demo.show_demo()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def init_handlers():
    dpg.create_context()

    def change_text(sender, app_data):
        dpg.set_value("text item", f"Mouse Button ID: {app_data}")

    def visible_call(sender, app_data):
        print("I'm visible")

    with dpg.item_handler_registry(tag="widget handler") as handler:
        dpg.add_item_clicked_handler(callback=change_text)
        dpg.add_item_visible_handler(callback=visible_call)

    with dpg.window(width=500, height=300):
        dpg.add_text("Click me with any mouse button", tag="text item")
        dpg.add_text("Close window with arrow to change visible state printing to console", tag="text item 2")

    # bind item handler registry to item
    dpg.bind_item_handler_registry("text item", "widget handler")
    dpg.bind_item_handler_registry("text item 2", "widget handler")

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def init_handlers_global():
    dpg.create_context()

    def change_text(sender, app_data):
        dpg.set_value("text_item", f"Mouse Button: {app_data[0]}, Down Time: {app_data[1]} seconds")

    with dpg.handler_registry():
        dpg.add_mouse_down_handler(callback=change_text)

    with dpg.window(width=500, height=300):
        dpg.add_text("Press any mouse button", tag="text_item")

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def init_polling():
    dpg.create_context()

    def change_text(sender, app_data):
        if dpg.is_item_hovered("text item"):
            dpg.set_value("text item", f"Stop Hovering Me, Go away!!")
        else:
            dpg.set_value("text item", f"Hover Me!")

    with dpg.handler_registry():
        dpg.add_mouse_move_handler(callback=change_text)

    with dpg.window(width=500, height=300):
        dpg.add_text("Hover Me!", tag="text item")

    dpg.create_viewport(title='Custom Title', width=800, height=600)
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
        # below replaces, start_dearpygui()
        while dpg.is_dearpygui_running():
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            updater()
            dpg.render_dearpygui_frame()

    @staticmethod
    def __log(prefix, sender, app_data, user_data):
        print(f"[{prefix}] sender: {sender}, app_data: {app_data}, user_data: {user_data}")

    # ------------------------------------------------------------------------------------------------------------------
    # private
    # ------------------------------------------------------------------------------------------------------------------
    def __init_prime_window(self, tag):
        with dpg.window(tag=tag):
            # Select methods block
            dpg.add_text(Settings.SELECT_ML_METHOD)
            dpg.add_radio_button(Settings.ML_METHODS, callback=self.__callback_change_learn_status)
            # Learn block
            with dpg.group(horizontal=True):
                dpg.add_button(label=Settings.LEARN, callback=self.__callback_learn)
                dpg.add_text("Some test result", tag=self.__teach_result)
            # Test block
            with dpg.group(horizontal=True):
                dpg.add_button(label=Settings.TEST)
                dpg.add_input_text(label=Settings.INPUT_VALUE_FOR_TEST)
            dpg.add_text("Some test result", tag=self.__test_result)
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
            dpg.set_value(self.__teach_result, Settings.ALREADY_LEARNED)
        else:
            dpg.set_value(self.__teach_result, Settings.NOT_LEARNED)
        pass

    def __callback_change_learn_status(self, sender, app_data, user_data):
        self.__log("__callback_change_learn_status", sender, app_data, user_data)
        self.__change_learn_status(app_data)

    def __callback_learn(self, sender, app_data, user_data):
        self.__log("__callback_learn", sender, app_data, user_data)
        self.__current_method = self.__get_save_by_label(app_data)
        self.__current_method.teach()
        self.__change_learn_status(app_data)

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
        self.__teach_result = Settings.TAG_LEARN_RESULT
        self.__test_result = Settings.TAG_TEST_RESULT
        self.__rf = Saves.MLSave("RF")
        self.__svm = Saves.MLSave("SVM")
        self.__knn = Saves.MLSave("KNN")
        self.__gbm = Saves.MLSave("GBM")
        self.__stacking = Saves.MLSave("Stacking")
        self.__current_method = self.__rf
        self.__counter = 1
        dpg.create_context()

    def init_gui(self):
        self.__init_prime_window(self.__prime_window_label)
        self.__init_viewport(self.__viewport_label, self.__viewport_width, self.__viewport_height)
        self.__init_frame_updater(self.__main_updater)
