from http.client import responses
import tkinter as tk
import customtkinter as ctk
import json
import tkinter as tk

class topBarFrame(ctk.CTkFrame):  # Corrected the inheritance
    def __init__(self, parent, request_handler):

        super().__init__(parent, corner_radius=0)
        self.s = request_handler
        self.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.grid_columnconfigure(4, weight=0)

        self.logo_label = ctk.CTkLabel(self, text="HHDbManager",
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.combobox_var = ctk.StringVar(value=self.get_tables()[0])  # set initial value
        self.combobox = ctk.CTkComboBox(self,
                                                  values=self.get_tables(),
                                                  command=parent.combobox_callback,
                                                  variable=self.combobox_var)
        self.combobox.grid(row=0, column=1, padx=0, pady=(20, 10), sticky="w")

        self.add_button = ctk.CTkButton(self, command=parent.add_entry, font=('Font Awesome 6 Free-Solid-900',20), text="\uf067", width=30)
        self.add_button.grid(row=0, column=3, padx=20, pady=(20, 10), sticky="e")
    #f120
        self.refresh_button = ctk.CTkButton(self, command=lambda: self.refresh_tables(parent), font=('Font Awesome 6 Free-Solid-900',20), text="\uf021", width=30)
        self.refresh_button.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="e")

        self.console_button = ctk.CTkButton(self, command=parent.create_console, font=('Font Awesome 6 Free-Solid-900', 20),text="\uf120", width=30)
        self.console_button.grid(row=0, column=4, padx=20, pady=(20, 10), sticky="e")

        self.settings_button = ctk.CTkButton(self, command=parent.generate_settings_menu,
                                            font=('Font Awesome 6 Free-Solid-900', 20), text="\uf013", width=30)
        self.settings_button.grid(row=0, column=5, padx=20, pady=(20, 10), sticky="e")

    def refresh_tables(self, parent):
        parent.generate_table(parent.s, parent.table_showing)
        parent.generate_side_bar()

    def get_tables(self):
        response = self.s.serverRequest("select * from information_schema.tables where table_schema = 'public'")
        tables = [];
        for table in response:
            tables.append(table['table_name'])
        return tables

class addWindow(ctk.CTkToplevel):
    def __init__(self, parent, request_handler, table):
        super().__init__(parent)
        self.s = request_handler
        self.title("Add: " + table)
        #self.attributes("-topmost", 1)
        self.wm_transient(parent)
        self.table = table
        response = self.s.serverRequest("SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '"+table+"'")
        #print(response)
        headers = []
        for column in response:
            try:
                needs_input = self.s.serverRequest(column['column_default'])
            except:
                headers.append(column['column_name'])
        self.grid_columnconfigure(len(headers), weight=0)
        self.entries = {}
        for col_idx, col_name in enumerate(headers):
            header = ctk.CTkLabel(self, text=col_name)
            input = ctk.CTkEntry(self)
            input.grid(row=1, column=col_idx, padx=5, pady=5)
            header.grid(row=0, column=col_idx, padx=5, pady=5)
            self.entries[col_name] = input
        add_button = ctk.CTkButton(self, text='Add', command=lambda: self.add_entry(parent))
        add_button.grid(row=3, column=0, columnspan =len(headers), padx=5, pady=(5, 5), sticky="nesw")

    def add_entry(self,parent):
        entry_field_names = '('
        entry_field_values = '('
        for entry in self.entries:
            entry_field_names += entry + ","
            entry_field_values += "'" + self.entries[entry].get() + "',"

        entry_field_names = entry_field_names[:-1]
        entry_field_values = entry_field_values[:-1]
        entry_field_names += ')'
        entry_field_values += ')'

        response = self.s.serverRequest('INSERT INTO '+self.table+" " + entry_field_names + " VALUES " + entry_field_values)
        parent.generate_table(parent.s, parent.table_showing)
        if response["message"].split()[:2] == ['SQL', 'Error']:
            eB = errorBox(self, self.s, response["message"])
        else:
            self.destroy()

class generateTable(ctk.CTkFrame):
    def __init__(self, parent, request_handler, table_name):
        super().__init__(parent)
        self.s = request_handler
        self.columns = self.get_headers(table_name)
        data = self.get_data(table_name)
        self.grid_columnconfigure(len(self.columns)+1, weight=1)

        for col_idx, col_name in enumerate(self.columns):
            header = ctk.CTkLabel(self, text=col_name)
            header.grid(row=0, column=col_idx, padx=5, pady=5)

        self.table_rows = []  # To keep track of row frames for deletion
        for row_id, row_data in enumerate(data, start=1):
            self.individual_rows = []
            for col_idx, value in enumerate(row_data):
                entry = ctk.CTkLabel(self, text=value)
                entry.grid(row=row_id, column=col_idx, padx=5, pady=5)
                self.individual_rows.append(entry)

            # Create Edit and Delete buttons
            #edit_button = ctk.CTkButton(self, text="Edit", command=lambda row_id=row_id: self.edit_row(row_id))
            delete_button = ctk.CTkButton(self, font=('Font Awesome 6 Free-Solid-900',20), text="\uf2ed", command=lambda row_id=row_id: self.delete_row(row_id,parent), fg_color='red', hover_color='#800000')

            #edit_button.grid(row=row_id, column=len(self.columns) + 1, padx=5, pady=5, sticky = 'e')
            delete_button.grid(row=row_id, column=len(self.columns) + 2, padx=5, pady=5, sticky = 'e')

            # Store row frame for future reference (deletion)

            #self.individual_rows.append(edit_button)
            self.individual_rows.append(delete_button)
            self.table_rows.append(self.individual_rows)



    def get_headers(self, table_name):
        response = self.s.serverRequest("SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '"+table_name+"'")
        headers = []
        for column in response:
            headers.append(column['column_name'])
        return headers

    def get_data(self, table_name):
        columns = self.get_headers(table_name)
        response = self.s.serverRequest("SELECT * FROM "+table_name)
        dataList = []
        #print(columns)
        try:
            for tables in response:
                dataEntry = []
                for column in columns:
                    dataEntry.append(tables[column])
                dataList.append(dataEntry)
        except:
            #print('empty table')
            pass
        return dataList

    def edit_row(self, row_id):
        #print(f"Editing row {row_id}")
        pass

    # Function to delete a row
    def delete_row(self, row_id,parent):
        #print(f"Deleting row {row_id}")
        #print(self.table_rows)
        # # Here, you can remove the row from the table (e.g., by destroying the frame)

        #print(self.table_rows[row_id-1][0].cget("text"))
        response = self.s.serverRequest('DELETE FROM '+parent.table_showing+' WHERE '+self.columns[0] +' = ' + str(self.table_rows[row_id-1][0].cget("text")))
        #print(response["message"].split()[:2])
        if response["message"].split()[:2] == ['SQL', 'Error']:
            eB = errorBox(self, self.s, response["message"])
        else:
            for tableElement in self.table_rows[row_id - 1]:
                tableElement.destroy()
            pass

class generateConsole(ctk.CTkToplevel):
    def __init__(self, request_handler):
        super().__init__()
        self.s = request_handler
        self.title("SQL Console")
        #self.geometry("600x400")

        self.attributes("-topmost", 1)
        self.grid_rowconfigure((0,1), weight=1)
        # Frame for the console output
        self.output_frame = ctk.CTkFrame(self, width=580, height=300)
        self.output_frame.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="nesw")
        #self.output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Console output (tk.Text for better tag support)
        self.console_output = tk.Text(
            self.output_frame,
            wrap="word",
            state="disabled",
            bg="#2e2e2e",
            fg="white",
            font=("Consolas", 12)
        )
        #self.console_output.pack(pady=10, padx=10, fill="both", expand=True)

        # Configure text tags
        self.console_output.tag_configure("info", foreground="yellow")
        self.console_output.tag_configure("error", foreground="red")
        self.console_output.tag_configure("warning", foreground="yellow")
        self.console_output.tag_configure("user", foreground="yellow")
        self.console_output.tag_configure("server", foreground="green")
        self.console_output.tag_configure("text", foreground="white")
        self.console_output.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="nesw")

        # Console input (CTkEntry)
        self.console_input = ctk.CTkEntry(self, placeholder_text="Type your command here...")
        self.console_input.grid(row=1, column=0, padx=5, pady=(5, 5), sticky="nesw")
        #self.console_input.pack(pady=10, padx=10, fill="x", side="bottom")  # Ensure it stays at the bottom

        # Bind Enter key to handle input
        self.console_input.bind("<Return>", self.handle_input)

        # Add a sample system message
        self.write_to_console("System", "Welcome to SQL Console!", "info")

    def write_to_console(self, client, message, tag="info"):
        """Write a message to the console with a specific tag for the client and a default 'text' tag for the rest."""
        # Enable the textbox to modify content
        self.console_output.configure(state="normal")

        # Insert the client name with its specific tag
        start_index = self.console_output.index("end-1c")  # Get the current end of the content
        self.console_output.insert("end", f"{client}: ")  # Insert client name (e.g., "server: ")
        end_index = self.console_output.index("end-1c")  # Get the position after inserting the client name
        self.console_output.tag_add(tag, start_index, end_index)  # Tag for the client name (e.g., 'server')

        # Insert the rest of the message with the 'text' tag
        self.console_output.insert("end", f"{message}\n")  # Insert the rest of the message
        start_index = self.console_output.index("end-1c")  # Get the position after the entire message
        end_index = self.console_output.index("end-1c")  # Position after the rest of the message
        self.console_output.tag_add("text", start_index, end_index)  # 'text' tag for the rest of the message

        # Disable editing again
        self.console_output.configure(state="disabled")
        self.console_output.see("end")  # Scroll to the end of the text

    def handle_input(self, event):
        """Handle user input when Enter is pressed."""
        user_input = self.console_input.get()
        if user_input.strip():

            self.write_to_console(f"User",  f"{user_input}", "user")
            self.console_input.delete(0, "end")  # Clear the input box
            self.process_user_command(user_input)

    def process_user_command(self, command):
        """Send the user command to the server and handle the response."""
        response = self.s.serverRequest(command.strip())
        if isinstance(response, dict) and "message" in response:
            if response["message"].split()[:2] == ['SQL', 'Error']:
                self.write_to_console(f"Server", f"{response['message']}", "error")
            else:
                self.write_to_console(f"Server", f"{response['message']}", "server")
        else:
            self.write_to_console(f"Server",  f"{response}", "server")

class errorBox(ctk.CTkToplevel):
    def __init__(self, parent, request_handler, error_message):
        super().__init__(parent)
        self.s = request_handler
        self.error_message = error_message
        self.attributes("-topmost", 1)
        self.grid_rowconfigure((0,1), weight=1)
        error_label = ctk.CTkLabel(self, text=error_message)
        error_label.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="nsew")
        exit_button = ctk.CTkButton(self, text="Exit", command=lambda: self.destroy())
        exit_button.grid(row=1, column=0, padx=5, pady=(5, 5), sticky="nsew")

class settingsMenu(ctk.CTkToplevel):
    def __init__(self, parent, request_handler):
        super().__init__(parent)
        self.s = request_handler
        self.title("Add settings")
        self.wm_transient(parent)

        self.menue_frame = ctk.CTkFrame(self)
        self.menue_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.menue_frame.grid_columnconfigure((0,1), weight=1)
        self.menue_frame.grid_rowconfigure((0,1,3), weight=1)

        self.mode_label = ctk.CTkLabel(self.menue_frame, text="Mode")
        self.mode_label.grid(row=0, column=0, padx=5, pady=(5, 5))
        self.mode_combo_box = ctk.CTkOptionMenu(self.menue_frame, values=["Light", "Dark", "System"],
                                                                       command=parent.change_appearance_mode_event)
        self.mode_combo_box.grid(row=0, column=1, padx=5, pady=(5, 5))

        self.scale_label = ctk.CTkLabel(self.menue_frame, text="Scale")
        self.scale_label.grid(row=1, column=0, padx=5, pady=(5, 5))

        self.scale_combo_box = ctk.CTkOptionMenu(self.menue_frame, values=["80%", "90%", "100%", "110%", "120%"],
                       command=parent.change_scaling_event)
        self.scale_combo_box.grid(row=1, column=1, padx=5, pady=(5, 5))

        self.close_button = ctk.CTkButton(self.menue_frame, text="Close", command=lambda: self.destroy())
        self.close_button.grid(row=3, column=0, columnspan = 2, padx=5, pady=(5, 5))