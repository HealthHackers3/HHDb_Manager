import tkinter
import tkinter.messagebox
import customtkinter
import request_handler
from generate_ui_element import *


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.s = request_handler.HHackServer()
        self.table_showing = 'users'
        # configure window
        self.title("HHackDb Admin Manager.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)

        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.generate_side_bar()
        self.generate_table(self.s, self.table_showing)
        #self.generate_table(self.s, 'users')

    def generate_side_bar(self):
        tbF = topBarFrame(self, self.s)

    def add_entry(self):
        aw = addWindow(self, self.s, self.table_showing)

    def combobox_callback(self, choice):
        self.table_showing = choice
        self.generate_table(self.s, choice)

    def create_console(self ):
        try:
            self.console.destroy()
        except:
            pass
        self.console = generateConsole(self.s)

    def generate_table(self, s, table_name):
        #print('I am the table man, I come from table way')
        table = generateTable(self, s, str(table_name))
        table.grid(row=1, column=0, sticky="nsew", rowspan=2, columnspan=4, padx=20, pady=(20, 10))

    def generate_settings_menu(self):
        sm = settingsMenu(self, self.s)
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    app = App()
    app.mainloop()