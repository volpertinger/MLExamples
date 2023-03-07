import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import UI.Settings as Settings


def init_demo():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=600)

    demo.show_demo()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def init_basic():
    dpg.create_context()
    dpg.create_viewport(title='Machine learning examples', width=600, height=200)
    dpg.setup_dearpygui()

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")

    dpg.show_viewport()

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        print("this will run every frame")
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


def init_prime():
    dpg.create_context()

    with dpg.window(tag="Primary Window"):
        dpg.add_text("Hello, world")

    dpg.create_viewport(title='Custom Title', width=600, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
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
    # private
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __init_viewport(label, width, height):
        dpg.create_viewport(title=label, width=width, height=height)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    @staticmethod
    def __init_prime_window(tag):
        with dpg.window(tag=tag):
            dpg.add_text("Hello, world")
        dpg.set_primary_window(tag, True)

    @staticmethod
    def __init_frame_updater(updater):
        # below replaces, start_dearpygui()
        while dpg.is_dearpygui_running():
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            updater()
            dpg.render_dearpygui_frame()

    @staticmethod
    def __main_updater():
        print("UI is running")

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
        self.viewport_width = width
        dpg.create_context()

    @staticmethod
    def deactivate():
        dpg.destroy_context()

    def init_gui(self):
        self.__init_viewport(self.__viewport_label, self.viewport_width, self.__viewport_height)
        self.__init_prime_window(self.__prime_window_label)
        self.__init_frame_updater(self.__main_updater)