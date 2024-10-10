import os
import customtkinter as ctk
import tkinter as tk
from tkinter import END
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import csv
import time
import subprocess

r_script = "GISAIDR_RUN.R"
ctk.set_appearance_mode("system")
class Login_Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.title("LOGIN")
        self.UsernameEntry = ctk.CTkEntry(self)
        self.PasswordEntry = ctk.CTkEntry(self, show="✲")
        self.DatabaseEntry = ctk.CTkOptionMenu(self, values=["EpiCoV", "EpiCox", "EpiRSV"])
        self.MenuLabel = ctk.CTkLabel(self, text="  GISAIDR INTERFACER GUI | V.0.1", font=("Arial", 30, 'bold'), wraplength=350)
        self.Login_Button = ctk.CTkButton(self, text="Login", command=self.login)
        self.Warning_Label = ctk.CTkLabel(self, text="Error: one or more fields empty, please try again.", font=("Arial", 16, "bold"), text_color="red")
        self.stored_login()
        self.create_widgets()

    def create_widgets(self):
        for i in range(6):
            self.columnconfigure(i, weight=1)
        for i in range(20):
            self.rowconfigure(i, weight=1)
        self.UsernameEntry.grid(row=10, column=2, sticky="w")
        self.create_label_with_field("Username:  ", 10, 1, "e")
        self.PasswordEntry.grid(row=11, column=2, sticky="w")
        self.create_label_with_field("Password:  ", 11, 1, "e")
        self.DatabaseEntry.grid(row=12, column=2, sticky="w")
        self.create_label_with_field("Database:  ", 12, 1, "e")
        self.MenuLabel.grid(row=2, column=1, columnspan=2, rowspan=4, sticky='nsew')
        self.Login_Button.grid(row=14, column=1, columnspan=2)

    def create_label_with_field(self, text, input_row, input_col, stick):
        label = ctk.CTkLabel(self, text=text, font=("Arial", 16))
        label.grid(row=input_row, column=input_col, sticky=stick)
    def login(self):
        username = self.UsernameEntry.get().strip()
        password = self.PasswordEntry.get().strip()
        database = self.DatabaseEntry.get().strip()
        if username and password:
            try:
                with open("credentials.txt", "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                lines=[]
            while len(lines) < 3:
                lines.append("\n")
            lines[0] = f"{username}\n"
            lines[1] = f"{password}\n"
            lines[2] = f"{database}\n"
            with open("credentials.txt", "w") as file:
                file.writelines(lines)
                print("Data written successfully.")
            self.after(200, self.destroy)
            main_app = App()
            main_app.bind_all('<Button>', change_focus)
            main_app.mainloop()
        else:
            self.Warning_Label.grid(row=8, column=1, columnspan=2)

    def stored_login(self):
        if os.path.exists("credentials.txt"):
            try:
                with open("credentials.txt", "r") as file:
                    lines = file.readlines()
                    if len(lines) >= 2 and lines[0].strip() and lines[1].strip():
                        self.UsernameEntry.insert(0, lines[0].strip())
                        self.PasswordEntry.insert(0, lines[1].strip())
                        print("Data loaded successfully.")
                    else:
                        print("Login data is incomplete.")
            except Exception as e:
                print(f"Error reading the file: {e}")
        else:
            print("No login data file found.")



class FileWatcher(FileSystemEventHandler):
    def __init__(self, gui_instance):
        self.gui_instance = gui_instance
        self.last_modified_time = None
        
    def on_modified(self, event):
        if event.src_path == os.path.abspath("GISAID_search_summary.csv"):
            current_time = time.time()
            if self.last_modified_time is None or current_time - self.last_modified_time > 2:
                self.last_modified_time = current_time
                print("GISAID_search_summary.csv has been modified.")
                self.gui_instance.update_gui()

class InputFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master)
        self.app_instance = app_instance
        self.configure(width=250, height=580)
        self.frame_label = ctk.CTkLabel(self, text="Inputs | Run", font=("Arial", 20, "bold"), fg_color=self.cget("fg_color"))
        self.frame_label.place(relx=0.5, y=30, anchor="center")

        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="", command=self.switch_event,
                                              variable=self.switch_var, onvalue="on", offvalue="off", switch_width=100, switch_height=50)
        self.switch.place(x=75, y=100)
        self.data_nickname = self.create_textbox_with_label("Data Nickname", 235, 250)
        self.start_date = self.create_textbox_with_label("Start Date", 305, 320)
        self.end_date = self.create_textbox_with_label("End Date", 375, 390)
        self.locations = self.create_textbox_with_label("Geographical Locations", 445, 460)
        self.amino_acids = self.create_textbox_with_label("Amino Acids Substitutions", 515, 530)
        self.Warning_Label = ctk.CTkLabel(self, text="Error: one or more fields empty", font=("Arial", 15, "bold"), text_color="red")

    def create_textbox_with_label(self, label_text, label_y, entry_y):
        label = ctk.CTkLabel(self, text=label_text, font=("Arial", 12, "bold"))
        label.place(relx=0.5, y=label_y, anchor="center")

        textbox = ctk.CTkEntry(self, width=200, height=40)
        textbox.place(x=25, y=entry_y)
        return textbox

    def switch_event(self):
        if self.switch_var.get() == "on":
            if self.data_nickname.get() and self.start_date.get() and self.end_date.get() and self.locations.get() and self.amino_acids.get():
                self.after(100, self.run_processes)
                self.Warning_Label.destroy()
            else:
                print("Error: One or more input fields empty.")
                self.after(200, self.switch.deselect)
                self.Warning_Label.place(x=10, y=175)

    def run_processes(self):
        self.append_inputs_and_gisaid_to_longterm_storage()

    def append_inputs_and_gisaid_to_longterm_storage(self):
        data_nickname = self.data_nickname.get().strip()
        start_date = self.start_date.get().strip()
        end_date = self.end_date.get().strip()
        locations_diff = self.locations.get().strip()
        amino_acids = self.amino_acids.get().strip()
        input_row = [data_nickname, start_date, end_date, locations_diff, amino_acids]

        try:
            with open("input_data.txt", "w") as file:
                file.write(f"{data_nickname}\n{start_date}\n{end_date}\n{locations_diff}\n{amino_acids}\n")
            self.after(200, self.run_r_script_and_append_data, input_row)
        except Exception as e:
            print(f"Error writing to input_data.txt: {e}")

    def run_r_script_and_append_data(self, input_row):
        try:
            subprocess.run(["Rscript", r_script])
            with open("GISAID_search_summary.csv", "r") as gisaid_file:
                csv_reader = csv.reader(gisaid_file)
                gisaid_data = list(csv_reader)
            if gisaid_data and len(gisaid_data[0]) > 0:
                total_viral_count = gisaid_data[0][0]
                input_row.append(total_viral_count)
                with open("longterm_storage.csv", "a", newline="") as longterm_file:
                    csv_writer = csv.writer(longterm_file)
                    csv_writer.writerow(input_row)
                self.app_instance.update_gui()
            else:
                print("No data to append from GISAID.")
        except Exception as e:
            print(f"Error running R script or appending data: {e}")
        self.clear_inputs()


    def clear_inputs(self):
        self.data_nickname.delete(0, ctk.END)
        self.start_date.delete(0, ctk.END)
        self.end_date.delete(0, ctk.END)
        self.locations.delete(0, ctk.END)
        self.amino_acids.delete(0, ctk.END)
        self.after(200, self.switch.deselect)

#
# TABLE CLASS
#

class TableFrame(ctk.CTkFrame):
    def __init__(self, master, data, headers):
        super().__init__(master)
        self.configure(width=700, height=400)
        self.data = data
        self.headers = headers
        self.entries = []
        self.canvas = tk.Canvas(self, width=680, height=400, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=30)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y", padx=5, pady=5)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.header_frame = tk.Frame(self, bg="lightgray")
        self.header_frame.place(x=10, y=10, width=680, height=20)

#
# CREATE HEADER CELLS
#

        for j, header in enumerate(headers):
            header_entry = tk.Entry(self.header_frame, width=16, fg='black', font=("Arial", 12), highlightthickness=0, readonlybackground="white", bd=0, justify="center")
            header_entry.grid(row=0, column=j, sticky="nsew", padx=0, pady=0, ipady=2)
            header_entry.insert(tk.END, header)
            header_entry.config(state="readonly")
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        total_columns = len(headers)

#
# CREATE THE TABLES
#

        for i, row_data in enumerate(self.data):
            row_entries = []
            for j in range(len(self.headers)):
                e = tk.Entry(self.scrollable_frame, width=16, fg='white', font=("Arial", 12), highlightthickness=0, bd=0, justify="center")
                e.grid(row=i, column=j, sticky="nsew", ipady=4)
                e.insert(tk.END, row_data[j] if j < len(row_data) else "")
                e.config(state="readonly")
                row_entries.append(e)
            self.entries.append(row_entries)
        for j in range(len(self.headers)):
            self.scrollable_frame.grid_columnconfigure(j, weight=1)
        for i in range(len(self.data)):
            self.scrollable_frame.grid_rowconfigure(i, weight=1)
    def populate_table(self):
        self.entries = []
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        total_columns = len(self.headers)

        for j, header in enumerate(self.headers):
            header_entry = tk.Entry(self.header_frame, width=16, fg='black', font=("Arial", 12),
                                    highlightthickness=0, readonlybackground="white", bd=0, justify="center")
            header_entry.grid(row=0, column=j, sticky="nsew", padx=0, pady=0, ipady=2)
            header_entry.insert(tk.END, header)
            header_entry.config(state="readonly")

        for i, row_data in enumerate(self.data):
            row_entries = []
            for j in range(total_columns):
                e = tk.Entry(self.scrollable_frame, width=16, fg='white', font=("Arial", 12), highlightthickness=0, bd=0, justify="center")
                e.grid(row=i, column=j, sticky="nsew", ipady=4)
                e.insert(tk.END, row_data[j] if j < len(row_data) else "")
                e.config(state="readonly")

                row_entries.append(e)
            self.entries.append(row_entries)
        for j in range(total_columns):
            self.scrollable_frame.grid_columnconfigure(j, weight=1)
        for i in range(len(self.data)):
            self.scrollable_frame.grid_rowconfigure(i, weight=1)

    def rebuild_table(self):
        self.populate_table()

#
# SCROLL EXPAND
#

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

#
# COMPARE LINES
#

    def toggle_comparison(self, compare):
        if compare:
            for i, row_entries in enumerate(self.entries):
                for entry in row_entries:
                    if entry.winfo_exists():
                        entry.config(readonlybackground="#303030")

            for i in range(len(self.data) - 1):
                try:
                    current_total_count = int(self.data[i][5])
                    next_total_count = int(self.data[i + 1][5]) 
                except (ValueError, TypeError, IndexError):
                    continue
                for entry in self.entries[i]:
                    if entry.winfo_exists():
                        if next_total_count > current_total_count:
                            entry.config(readonlybackground="red")
                        elif next_total_count < current_total_count:
                            entry.config(readonlybackground="green")
                        else:
                            entry.config(readonlybackground="blue")
        else:
            for i, row_entries in enumerate(self.entries):
                for entry in row_entries:
                    if entry.winfo_exists():
                        entry.config(readonlybackground="#303030")

#
# BUILD GUI
#

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GISAID Interfacer | V.0.1")
        self.geometry("1000x600")
        self.input_frame = InputFrame(self, self)
        headers = ["Data Nickname", "Start Date", "End Date", "Location", "AA Substitutions", "Total Count"]
        self.input_frame.place(x=10, y=10)
        table_data = []
        self.table_frame = TableFrame(self, table_data, headers)
        self.table_frame.place(x=270, y=10)
        with open("input_data.txt", "r") as file:
            data = file.readlines()
            table_data = [line.strip().split(',') for line in data]
        self.compare_var = tk.BooleanVar(value=False)
        compare_checkbox = ctk.CTkCheckBox(self, text="Toggle Comparison", variable=self.compare_var, command=self.on_compare_toggle)
        compare_checkbox.place(x=270, y=565)
        self.wipe_data_switch = ctk.CTkSwitch(self, text="", command=self.check_wipe)
        self.wipe_data_switch.place(x=270, y=472)
        self.wipe_all_data = self.create_textbox_with_label_2("Confirm Data Wipe")
        self.placeholdertext = 'Type "DELETE ALL DATA" to confirm'
        self.wipe_all_data.insert(0, self.placeholdertext)
        self.wipe_all_data.configure(fg_color='#343638',text_color='white')
        self.wipe_all_data.bind("<FocusIn>", self.on_focus_in)
        self.wipe_all_data.bind("<FocusOut>", self.on_focus_out)
        self.update_gui()
        self.setup_file_watcher()

#
# FUNC. RUNS
#
    def setup_file_watcher(self):
        event_handler = FileWatcher(self)
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(os.path.abspath("GISAID_search_summary.csv")), recursive=False)
        observer.start()
    def update_gui(self):
        try:
            with open("input_data.txt", "r") as input_file:
                data_nickname = input_file.readline().strip()

            with open("longterm_storage.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                rows = list(csv_reader)
                
            if len(rows) == 0 or len(rows[0]) < 6:
                print("Error: The long-term storage file is empty or doesn't have enough data.")
                return
            self.table_frame.data.clear()
            for csv_row in rows:
                if len(csv_row) >= 6:
                    new_row = [
                        csv_row[0],
                        csv_row[1],
                        csv_row[2],
                        csv_row[3],
                        csv_row[4],
                        csv_row[5]
                    ]
                    
                    self.table_frame.data.append(new_row)

            self.table_frame.rebuild_table()
        except Exception as e:
            print(f"Error updating table: {e}")

    def print_inputs(self):
        self.input_frame.get_inputs()



    def create_textbox_with_label_2(self, label_text):
        label = ctk.CTkLabel(self, text=label_text, font=("Arial", 12, "bold"))
        label.place(x=315, y=469)
        label.configure(text_color="red")

        textbox = ctk.CTkEntry(self, width=240, height=20)
        textbox.place(x=265, y=495)
        return textbox
    def on_compare_toggle(self):
        self.table_frame.toggle_comparison(self.compare_var.get())
    def on_focus_in(self, event):
        if self.wipe_all_data.get() == self.placeholdertext:
            self.wipe_all_data.delete(0, ctk.END)
            self.wipe_all_data.configure(fg_color="black")
    def on_focus_out(self, event):
        if self.wipe_all_data.get() == "":
            self.wipe_all_data.insert(0, self.placeholdertext)
            self.wipe_all_data.configure(fg_color='#343638')
    def check_wipe(self):
        entered_text = self.wipe_all_data.get()
        if entered_text == 'DELETE ALL DATA':
            try:
                wipe_file = open("longterm_storage.csv", "w")
                wipe_file.close()
                self.table_frame.data.clear()
                self.table_frame.rebuild_table()
                self.after(200, self.wipe_data_switch.deselect)
                self.wipe_all_data.delete(0, ctk.END)
            except Exception as e:
                print(f"Error wiping storage file: {e}")
        else:
            self.after(200, self.wipe_data_switch.deselect)
            print("Captcha not answered")
def change_focus(event):
    event.widget.focus_set()

if __name__ == "__main__":
    app = Login_Window()
    app.bind_all('<Button>', change_focus)
    app.mainloop()
