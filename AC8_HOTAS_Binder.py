import os
import shutil
import tkinter as  tk
from tkinter import filedialog, messagebox, ttk
import configparser
import json

STICK_BUTTONS = {
    1: "Trigger",
    2: "Button A",
    3: "Button B",
    5: "Button D",
    6: "Pinky Switch"
    }

THROTTLE_BUTTONS = {
    1: "Button E",
    2: "F Push (Top Rotary Click)",
    3: "G Push (Bottom Rotary Click)",
    4: "Button I",
    5: "Button H",
    6: "SW 1",
    7: "SW 2",
    8: "SW 3",
    9: "SW 4",
    10: "SW 5",
    11: "SW 6",
    12: "TGL 1 Up",
    13: "TGL 1 Down",
    14: "TGL 2 Up",
    15: "TGL 2 Down",
    16: "TGL 3 Up",
    17: "TGL 3 Down",
    18: "TGL 4 Up",
    19: "TGL 4 Down",
    28: "K1 Up",
    29: "K1 Down",
    30: "Scroll FWD",
    31: "Scroll BCK",
    33: "SLD (Slider Switch)"
    }

class Ace8X56Editor:
    def __init__(self, root):
        self.root = root
        self.root.title("Ace Combat 8 - X56 Keybind Configurator")
        self.root.geometry("780x650")

        self.config = configparser.ConfigParser(
            delimiters=('=',),
            comment_prefixes=None,
            inline_comment_prefixes=None,
            strict=False,
            interpolation=None
            )
        self.config.optionxform = str
        self.file_path = ""

        local_app_data = os.environ.get("LOCALAPPDATA", "")
        self.default_dir = os.path.join(local_app_data, "BANDAI NAMCO Entertainment", "ACE COMBAT 8", "Saved", "Config", "Windows")

        self.create_widgets()

    def create_widgets(self):
        file_frame = tk.Frame(self.root, pady=10)
        file_frame.pack(fill=tk.X)

        self.btn_load = tk.Button(file_frame, text="Open Config File", command=self.load_file, bg="#2b2b2b", fg="white")
        self.btn_load.pack(side=tk.LEFT, padx=10)

        self.lbl_file = tk.Label(file_frame, text="No configuration loaded", fg="gray", wraplength=400, justify="left")
        self.lbl_file.pack(side=tk.LEFT, padx=10)

        self.btn_save = tk.Button(file_frame, text="Save Config", command=self.save_file, state=tk.DISABLED, bg="#1a5f7a", fg="white")
        self.btn_save.pack(side=tk.RIGHT, padx=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.stick_tab = ttk.Frame(self.notebook)
        self.throttle_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.stick_tab, text="X56 Flight Stick")
        self.notebook.add(self.throttle_tab, text="X56 Throttle")

        self.entries = {
            "LT_SaitekProFlightX56RhinoStick": {},
            "LT_SaitekProFlightX56RhinoThrottle": {}
            }

    def load_file(self):
        initial_dir = self.default_dir if os.path.exists(self.default_dir) else os.path.expanduser("~")

        self.file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select Ace Combat 8 Input Config File",
            filetypes=[("Ace Combat 8 Config", "*.ini"), ("All Files", "*.*")]
            )
        if not self.file_path:
            return

        try:
            self.config.read(self.file_path)
            self.lbl_file.config(text=self.file_path, fg="green")

            for widget in self.stick_tab.winfo_children(): widget.destroy()
            for widget in self.throttle_tab.winfo_children(): widget.destroy()

            self.populate_tab("LT_SaitekProFlightX56RhinoStick", self.stick_tab, STICK_BUTTONS)
            self.populate_tab("LT_SaitekProFlightX56RhinoThrottle", self.throttle_tab, THROTTLE_BUTTONS)

            self.btn_save.config(state=tk.NORMAL)
            messagebox.showinfo("Loaded", "Ace Combat 8 config loaded successfully.")
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to open config:\n{str(e)}")

    def populate_tab(self, section_name, tab_frame, hardware_map):
        if not self.config.has_section(section_name):
            tk.Label(tab_frame, text=f"Missing section data inside file: [{section_name}]", fg="red").pack(pady=20)
            return

        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        btn_options = {}
        for k, v in hardware_map.items():
            btn_options[f"ID {k} ({v})"] = k
        btn_display_list = ["0 (Unassigned)"] + list(btn_options.keys())

        row = 0
        for key, value in self.config.items(section_name):
            if key in ["DeviceID", "DeviceInputItemMap_Platform"]:
                continue

            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            value = value.replace('\\"', '"')

            try:
                data = json.loads(value)
                settings_data = data["inputSettings"]

                if isinstance(settings_data, list) and len(settings_data):
                    settings = settings_data[0]
                else:
                    settings = settings_data if isinstance(settings_data, dict) else {}

                input_type = settings.get("inputType", "None")
                btn_index = settings.get("buttonIndex", 0)
                axis_opt = settings.get("axisInputOption", "Standard")
            except Exception:
                input_type, btn_index, axis_opt = "None", 0, "Standard"

            game_action = key.replace("DeviceInputItemMap_", "")

            lbl_action = tk.Label(scrollable_frame, text=f"{game_action}:", font=("Arial", 9, "bold"), width=22, anchor="w")
            lbl_action.grid(row=row, column=0, padx=10, pady=6, sticky="w")

            inputs_frame = tk.Frame(scrollable_frame)
            inputs_frame.grid(row=row, column=1, padx=5, pady=6, sticky="w")

            type_var = tk.StringVar(value=input_type)
            type_combo = ttk.Combobox(inputs_frame, textvariable=type_var, values=["Button", "POV_U", "POV_D", "POV_L", "POV_R", "X", "Y", "Rz", "Rx", "Ry", "None"], width=8, state="readonly")
            type_combo.pack(side=tk.LEFT, padx=2)

            current_display = "0 (Unassigned)"
            for display_str, idx in btn_options.items():
                if idx == btn_index and input_type not in ["X", "Y", "Rz", "Rx", "Ry"]:
                    current_display = display_str
                    break

            btn_var = tk.StringVar(value=current_display)
            btn_combo = ttk.Combobox(inputs_frame, textvariable=btn_var, values=btn_display_list, width=28, state="readonly")
            btn_combo.pack(side=tk.LEFT, padx=5)

            tk.Label(inputs_frame, text="Axis Mod:").pack(side=tk.LEFT, padx=(5,0))
            opt_var = tk.StringVar(value=axis_opt)
            opt_combo = ttk.Combobox(inputs_frame, textvariable=opt_var, values=["Standard", "Reverse", "ReverseConvert"], width=14, state="readonly")
            opt_combo.pack(side=tk.LEFT, padx=2)

            self.entries[section_name][key] = (type_var, btn_var, opt_var, btn_options)
            row += 1

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def save_file(self):
        try:
            backup_path = f"{self.file_path}.bak"
            shutil.copy2(self.file_path, backup_path)

            for section_name, controls in self.entries.items():
                if not self.config.has_section(section_name):
                    continue

                for key, tracking_tuple in list(controls.items()):
                    type_var, btn_var, opt_var, btn_options = tracking_tuple

                    selected_str = btn_var.get()
                    btn_idx = btn_options.get(selected_str, 0)

                    if section_name == "LT_SaitekProFlightX56RhinoThrottle" and key == "DeviceInputItemMap_Throttle" and type_var.get() in ["X", "Y"]:
                        settings_list = [
                            {"inputType": "X", "buttonIndex": 0, "axisInputOption": opt_var.get(), "enableButtonIndex": 0, "disableButtonIndex": 0},
                            {"inputType": "Y", "buttonIndex": 0, "axisInputOption": opt_var.get(), "enableButtonIndex": 0, "disableButtonIndex": 0}
                            ]
                    else:
                        settings_list = [{
                            "inputType": type_var.get(),
                            "buttonIndex": btn_idx if type_var.get() not in ["X", "Y", "Rz", "Rx", "Ry"] else 0,
                            "axisInputOption": opt_var.get(),
                            "enableButtonIndex": 0,
                            "disableButtonIndex": 0
                            }]

                    json_payload = json.dumps({"inputSettings": settings_list})
                    double_escaped_json = json_payload.replace('"', '\\"')
                    escaped_payload = f'"{double_escaped_json}"'

                    self.config.set(section_name, key, escaped_payload)

            with open(self.file_path, "w") as configfile:
                self.config.write(configfile, space_around_delimiters=False)

            messagebox.showinfo("Saved", "Ace Combat 8 profile written successfully!")
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to save profile:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Ace8X56Editor(root)
    root.mainloop()