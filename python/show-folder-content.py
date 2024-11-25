import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pyperclip  # Import pyperclip for clipboard functionality

class FolderStructureTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Folder Structure Display Tool")
        self.geometry("700x600")
        self.configure(bg="#f5f5f5")  # Light gray background color
        self.resizable(False, False)  # Fixed window size

        # Title Label with modern font
        self.title_label = tk.Label(self, text="Folder Structure Display Tool", font=("Helvetica", 18, 'bold'), fg="#333")
        self.title_label.pack(pady=20)

        # Select Folder Button with modern styling
        self.select_folder_button = tk.Button(self, text="Select Folder", command=self.select_folder,
                                              font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat",
                                              padx=20, pady=10, bd=0, cursor="hand2")
        self.select_folder_button.pack(pady=10)

        # Include Hidden Folders Checkbutton
        self.include_hidden_var = tk.BooleanVar()
        self.include_hidden_check = tk.Checkbutton(self, text="Include Hidden Folders", variable=self.include_hidden_var,
                                                   font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
        self.include_hidden_check.pack(pady=5)

        # Save Output Checkbutton
        self.save_output_var = tk.BooleanVar()
        self.save_output_check = tk.Checkbutton(self, text="Save Output as Text File", variable=self.save_output_var,
                                                font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
        self.save_output_check.pack(pady=5)

        # Text widget to display folder structure with styling
        self.text_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=75, font=("Courier", 12),
                                                     bg="#f4f4f9", fg="#333", bd=0, padx=10, pady=10)
        self.text_display.pack(pady=20)

        # Copy Button with modern look
        self.copy_button = tk.Button(self, text="Copy", command=self.copy_to_clipboard, font=("Helvetica", 14),
                                     bg="#008CBA", fg="white", relief="flat", padx=20, pady=10, bd=0, cursor="hand2")
        self.copy_button.pack(pady=10)

        # Status bar for feedback
        self.status_label = tk.Label(self, text="Welcome! Select a folder to get started.", font=("Helvetica", 10),
                                     bg="#f5f5f5", fg="#777")
        self.status_label.pack(side="bottom", fill="x", pady=5)

        # Initialize folder path
        self.folder_path = ""

    def update_status(self, message):
        """Update the status bar with a new message"""
        self.status_label.config(text=message)

    def select_folder(self):
        """Open a folder selection dialog"""
        self.folder_path = filedialog.askdirectory()

        if self.folder_path:
            # Clear the text widget before displaying new folder structure
            self.text_display.delete(1.0, tk.END)
            self.update_status(f"Displaying structure of: {self.folder_path}")
            self.display_structure(self.folder_path)

    def display_structure(self, startpath):
        """Display the folder structure"""
        include_hidden = self.include_hidden_var.get()

        structure_output = ""
        for root, dirs, files in os.walk(startpath):
            # Skip hidden directories if the checkbox is unchecked
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
            
            depth = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * depth
            structure_output += f"{indent}{os.path.basename(root)}/\n"
            
            subindent = ' ' * 4 * (depth + 1)
            for file in files:
                structure_output += f"{subindent}{file}\n"

        # Display the structure in the text widget
        self.text_display.insert(tk.END, structure_output)

        # If the Save Output checkbox is checked, save the output to a text file
        if self.save_output_var.get():
            self.save_to_text_file(startpath, structure_output)

    def save_to_text_file(self, startpath, structure_output):
        """Save the folder structure to a text file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(structure_output)
            self.update_status(f"Folder structure saved to {file_path}")

    def copy_to_clipboard(self):
        """Copy the folder structure output to the clipboard"""
        structure_output = self.text_display.get(1.0, tk.END).strip()
        
        if structure_output:
            pyperclip.copy(structure_output)  # Copy to clipboard using pyperclip
            self.update_status("Folder structure copied to clipboard!")

# Run the application
if __name__ == "__main__":
    app = FolderStructureTool()
    app.mainloop()
