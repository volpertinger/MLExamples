import dearpygui.dearpygui as dpg
import dearpygui.demo as demo


def save_callback():
    print("Save Clicked")


def init_gui():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=600)

    demo.show_demo()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
