# main.py

import tkinter
from tkinter import filedialog, messagebox
import customtkinter
import os
import json
import subprocess

# Import the backend logic from our other file
from converter_logic import create_mod_jar, sanitize_mod_id

def get_git_version():
    """Gets the short commit hash from Git, or returns 'dev' as a fallback."""
    try:
        # Run the git command to get the short hash of the current commit (HEAD)
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'], 
            shell=True, 
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return commit_hash
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback if git is not installed or this is not a git repository
        return "dev"

__version__ = get_git_version()

# --- GUI Application Class ---

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    CONFIG_FILE = "config.json"

    def __init__(self):
        super().__init__()

        self.title(f"Datapack to Fabric Mod Converter (v{__version__})")
        self.geometry("640x780")

        self.grid_columnconfigure(0, weight=1)
        
        # Create all widgets
        self.setup_ui()
        
        # Load saved settings from config.json
        self.load_settings()

    def setup_ui(self):
        # ... (The UI setup methods from the previous step are broken out) ...
        self.setup_instructions_frame()
        self.setup_path_frame()
        self.setup_meta_frame()
        self.setup_dep_frame()
        
        self.convert_button = customtkinter.CTkButton(self, text="Convert to Mod", font=customtkinter.CTkFont(size=16, weight="bold"), command=self.convert_datapack, height=40)
        self.convert_button.grid(row=4, column=0, padx=10, pady=(10, 10), sticky="ew")

    def setup_instructions_frame(self):
        instructions_frame = customtkinter.CTkFrame(self, corner_radius=10)
        instructions_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        instructions_text = "How to Use:\n1. Select your datapack folder (icon and description will be auto-detected).\n2. Fill in or adjust the mod metadata below.\n3. Click 'Convert to Mod' to generate the .jar file."
        customtkinter.CTkLabel(instructions_frame, text=instructions_text, justify="left").pack(padx=10, pady=10, anchor="w")
    
    def setup_path_frame(self):
        path_frame = customtkinter.CTkFrame(self, corner_radius=10)
        path_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        path_frame.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(path_frame, text="Paths", font=customtkinter.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=3, pady=(5, 10))
        
        customtkinter.CTkLabel(path_frame, text="Datapack Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.datapack_entry = customtkinter.CTkEntry(path_frame, placeholder_text="Select your datapack folder...")
        self.datapack_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        customtkinter.CTkButton(path_frame, text="Browse...", width=100, command=self.select_datapack).grid(row=1, column=2, padx=10, pady=5)

        customtkinter.CTkLabel(path_frame, text="Output Directory:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.output_entry = customtkinter.CTkEntry(path_frame)
        self.output_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        customtkinter.CTkButton(path_frame, text="Browse...", width=100, command=self.select_output).grid(row=2, column=2, padx=10, pady=5)
        self.output_entry.insert(0, os.path.join(os.getcwd(), "output"))
        
        customtkinter.CTkLabel(path_frame, text="Mod Icon (optional):").grid(row=3, column=0, padx=10, pady=(5,10), sticky="w")
        self.icon_entry = customtkinter.CTkEntry(path_frame, placeholder_text="Auto-detected from pack.png")
        self.icon_entry.grid(row=3, column=1, padx=10, pady=(5,10), sticky="ew")
        customtkinter.CTkButton(path_frame, text="Browse...", width=100, command=self.select_icon).grid(row=3, column=2, padx=10, pady=(5,10))

    def setup_meta_frame(self):
        meta_frame = customtkinter.CTkFrame(self, corner_radius=10)
        meta_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        meta_frame.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(meta_frame, text="Fabric Mod Metadata", font=customtkinter.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(5, 10))

        self.name_entry = self._create_meta_entry(meta_frame, "Mod Name:", 1)
        self.id_entry = self._create_meta_entry(meta_frame, "Mod ID:", 2)
        self.version_entry = self._create_meta_entry(meta_frame, "Version:", 3, default_value="1.0.0")
        self.author_entry = self._create_meta_entry(meta_frame, "Author(s):", 4, placeholder="e.g., YourName, OtherName")
        self.desc_entry = self._create_meta_entry(meta_frame, "Description:", 5)
        
        licenses = ["CC0-1.0", "MIT License", "GNU GPLv3", "Apache License 2.0", "The Unlicense", "GNU LGPLv3", "Mozilla Public License 2.0"]
        customtkinter.CTkLabel(meta_frame, text="License:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.license_combo = customtkinter.CTkComboBox(meta_frame, values=licenses)
        self.license_combo.grid(row=6, column=1, padx=10, pady=(5,10), sticky="ew")
        self.license_combo.set("CC0-1.0")

    def setup_dep_frame(self):
        dep_frame = customtkinter.CTkFrame(self, corner_radius=10)
        dep_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        dep_frame.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(dep_frame, text="Dependencies", font=customtkinter.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(5, 10))

        customtkinter.CTkLabel(dep_frame, text="Minecraft Version:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mc_version_entry = customtkinter.CTkEntry(dep_frame, placeholder_text='e.g., ">=1.21" or "1.21.x"')
        self.mc_version_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.mc_version_entry.insert(0, ">=1.21")
        
        customtkinter.CTkLabel(dep_frame, text="Fabric Loader Version:").grid(row=2, column=0, padx=10, pady=(5,10), sticky="w")
        self.fabric_version_entry = customtkinter.CTkEntry(dep_frame, placeholder_text='e.g., ">=0.15.0"')
        self.fabric_version_entry.grid(row=2, column=1, padx=10, pady=(5,10), sticky="ew")
        self.fabric_version_entry.insert(0, ">=0.15.0")
        
    def _create_meta_entry(self, parent, label_text, row, default_value="", placeholder=""):
        customtkinter.CTkLabel(parent, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = customtkinter.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        if default_value:
            entry.insert(0, default_value)
        return entry

    # --- Event Handlers and App Logic ---

    def load_settings(self):
        """Loads settings from config.json if it exists."""
        try:
            with open(self.CONFIG_FILE, "r") as f:
                config = json.load(f)
            
            # Use .get() for safety in case a key is missing
            author = config.get("author", "")
            output_path = config.get("output_path", "")

            if author:
                self.author_entry.delete(0, customtkinter.END)
                self.author_entry.insert(0, author)
            
            if output_path and os.path.isdir(os.path.dirname(output_path)): # Check if path is valid
                self.output_entry.delete(0, customtkinter.END)
                self.output_entry.insert(0, output_path)

        except (FileNotFoundError, json.JSONDecodeError):
            # No config file found or it's invalid, just start with defaults
            pass

    def save_settings(self):
        """Saves current settings to config.json."""
        settings = {
            "author": self.author_entry.get(),
            "output_path": self.output_entry.get()
        }
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(settings, f, indent=4)

    def select_datapack(self):
        path = filedialog.askdirectory(title="Select Datapack Folder")
        if not path: return

        self.datapack_entry.delete(0, customtkinter.END)
        self.datapack_entry.insert(0, path)
        
        self.name_entry.delete(0, customtkinter.END)
        self.name_entry.insert(0, os.path.basename(path))
        self.id_entry.delete(0, customtkinter.END)
        self.id_entry.insert(0, sanitize_mod_id(os.path.basename(path)))

        mcmeta_path = os.path.join(path, "pack.mcmeta")
        if os.path.exists(mcmeta_path):
            try:
                with open(mcmeta_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    description = data.get("pack", {}).get("description", "")
                    if isinstance(description, dict): description = description.get("text", "")
                    self.desc_entry.delete(0, customtkinter.END)
                    self.desc_entry.insert(0, str(description))
            except Exception as e:
                print(f"Could not read pack.mcmeta: {e}")

        png_path = os.path.join(path, "pack.png")
        if os.path.exists(png_path):
            self.icon_entry.delete(0, customtkinter.END)
            self.icon_entry.insert(0, png_path)

    def select_output(self):
        path = filedialog.askdirectory(title="Select Output Directory")
        if path:
            self.output_entry.delete(0, customtkinter.END)
            self.output_entry.insert(0, path)

    def select_icon(self):
        path = filedialog.askopenfilename(title="Select Icon PNG", filetypes=[("PNG files", "*.png")])
        if path:
            self.icon_entry.delete(0, customtkinter.END)
            self.icon_entry.insert(0, path)

    def convert_datapack(self):
        datapack_path = self.datapack_entry.get()
        output_path = self.output_entry.get()

        if not os.path.isdir(datapack_path):
            messagebox.showerror("Error", "Invalid datapack folder path.")
            return

        if not os.path.isdir(output_path):
            try:
                os.makedirs(output_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return
                
        metadata = {
            "name": self.name_entry.get(), "id": sanitize_mod_id(self.id_entry.get()),
            "version": self.version_entry.get(), "authors": self.author_entry.get(),
            "description": self.desc_entry.get(), "license": self.license_combo.get(),
            "minecraft_version": self.mc_version_entry.get(), "fabricloader_version": self.fabric_version_entry.get()
        }

        if not all([metadata['name'], metadata['id'], metadata['version'], metadata['authors']]):
            messagebox.showerror("Error", "Please fill in all required metadata fields:\nMod Name, Mod ID, Version, Author(s)")
            return

        try:
            final_jar_path = create_mod_jar(datapack_path, output_path, metadata, self.icon_entry.get())
            messagebox.showinfo("Success", f"Mod JAR created successfully at:\n{final_jar_path}")
            # On success, save the settings
            self.save_settings()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during conversion: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    app = App()
    app.mainloop()