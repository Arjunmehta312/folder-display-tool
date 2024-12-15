import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pyperclip
import json
from datetime import datetime

class FolderStructureTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Folder Structure Display Tool")
        self.geometry("900x700")
        self.configure(bg="#f5f5f5")
        self.resizable(False, False)

        # Title Label
        self.title_label = tk.Label(self, text="Folder Structure Display Tool", font=("Helvetica", 18, 'bold'), fg="#333")
        self.title_label.pack(pady=20)

        # Top Frame for Options
        self.top_frame = tk.Frame(self, bg="#f5f5f5")
        self.top_frame.pack(pady=10)

        # Select Folder Button
        self.select_folder_button = tk.Button(self.top_frame, text="Select Folder", command=self.select_folder,
                                              font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat",
                                              padx=20, pady=5, cursor="hand2")
        self.select_folder_button.grid(row=0, column=0, padx=10)

        # Include Hidden Folders
        self.include_hidden_var = tk.BooleanVar()
        self.include_hidden_check = tk.Checkbutton(self.top_frame, text="Include Hidden Folders", variable=self.include_hidden_var,
                                                   font=("Helvetica", 10), bg="#f5f5f5")
        self.include_hidden_check.grid(row=0, column=1, padx=10)

        # Save As Dropdown
        self.save_as_label = tk.Label(self.top_frame, text="Save As:", font=("Helvetica", 10), bg="#f5f5f5")
        self.save_as_label.grid(row=0, column=2, padx=5)

        self.save_as_var = tk.StringVar(value="None")
        self.save_as_menu = ttk.Combobox(self.top_frame, textvariable=self.save_as_var, state="readonly",
                                         values=["None", "Text File", "HTML", "JSON"], font=("Helvetica", 10), width=15)
        self.save_as_menu.grid(row=0, column=3, padx=10)

        # Text Widget for Folder Structure
        self.text_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20, width=100, font=("Courier", 10),
                                                      bg="#f4f4f9", fg="#333", bd=0, padx=10, pady=10)
        self.text_display.pack(pady=10)

        # Search Bar
        self.search_frame = tk.Frame(self, bg="#f5f5f5")
        self.search_frame.pack(pady=5)

        self.search_label = tk.Label(self.search_frame, text="Search:", font=("Helvetica", 12), bg="#f5f5f5")
        self.search_label.pack(side="left", padx=5)

        self.search_entry = tk.Entry(self.search_frame, font=("Helvetica", 12), width=40)
        self.search_entry.pack(side="left", padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_in_structure,
                                       font=("Helvetica", 10), bg="#008CBA", fg="white", relief="flat")
        self.search_button.pack(side="left", padx=5)

        # Copy Button
        self.copy_button = tk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard, font=("Helvetica", 12),
                                     bg="#008CBA", fg="white", relief="flat", padx=20, pady=5, cursor="hand2")
        self.copy_button.pack(pady=10)

        # Status Bar
        self.status_label = tk.Label(self, text="Welcome! Select a folder to get started.", font=("Helvetica", 10),
                                     bg="#f5f5f5", fg="#777")
        self.status_label.pack(side="bottom", fill="x", pady=5)

    def update_status(self, message):
        self.status_label.config(text=message)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()

        if self.folder_path:
            self.text_display.delete(1.0, tk.END)
            self.update_status(f"Displaying structure of: {self.folder_path}")
            self.display_structure(self.folder_path)

    def display_structure(self, startpath):
        include_hidden = self.include_hidden_var.get()
        structure_output = ""

        for root, dirs, files in os.walk(startpath):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]

            depth = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * depth
            structure_output += f"{indent}{os.path.basename(root)}/\n"

            subindent = ' ' * 4 * (depth + 1)
            for file in files:
                structure_output += f"{subindent}{file}\n"

        self.text_display.insert(tk.END, structure_output)

        selected_save_as = self.save_as_var.get()
        if selected_save_as == "Text File":
            self.save_to_text_file(startpath, structure_output)
        elif selected_save_as == "HTML":
            self.export_as_html(structure_output)
        elif selected_save_as == "JSON":
            self.export_as_json(structure_output)

    def save_to_text_file(self, startpath, structure_output):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(structure_output)
            self.update_status(f"Folder structure saved to {file_path}")

    def copy_to_clipboard(self):
        structure_output = self.text_display.get(1.0, tk.END).strip()
        if structure_output:
            pyperclip.copy(structure_output)
            self.update_status("Folder structure copied to clipboard!")

    def search_in_structure(self):
        search_term = self.search_entry.get().strip()
        self.text_display.tag_remove("highlight", "1.0", tk.END)

        if search_term:
            idx = "1.0"
            while True:
                idx = self.text_display.search(search_term, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                end_idx = f"{idx}+{len(search_term)}c"
                self.text_display.tag_add("highlight", idx, end_idx)
                self.text_display.tag_config("highlight", background="yellow")
                idx = end_idx
            self.update_status(f"Search completed for '{search_term}'!")

    def export_as_html(self, structure_output=None):
        if structure_output is None:
            structure_output = self.text_display.get(1.0, tk.END).strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(f"<pre>{structure_output}</pre>")
            self.update_status(f"Folder structure exported as HTML to {file_path}")

    def export_as_json(self, structure_output=None):
        if structure_output is None:
            structure_output = self.text_display.get(1.0, tk.END).strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            structure_dict = {"folder_structure": structure_output.splitlines()}
            with open(file_path, 'w') as f:
                json.dump(structure_dict, f, indent=4)
            self.update_status(f"Folder structure exported as JSON to {file_path}")

if __name__ == "__main__":
    app = FolderStructureTool()
    app.mainloop()