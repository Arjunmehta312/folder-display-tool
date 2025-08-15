import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pyperclip
import json
from datetime import datetime
import platform

class FolderStructureTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Folder Structure Display Tool - Version 4")
        self.geometry("1000x800")
        self.configure(bg="#f5f5f5")
        self.resizable(True, True)  # Allow resizing for better viewing

        # Path length tracking
        self.max_path_length = 0
        self.long_paths = []
        self.invalid_paths = []
        
        # Windows path length limit
        self.windows_path_limit = 260
        self.is_windows = platform.system() == "Windows"

        # Title Label
        self.title_label = tk.Label(self, text="Folder Structure Display Tool - Version 4",
                                    font=("Helvetica", 18, 'bold'), fg="#333", bg="#f5f5f5")
        self.title_label.pack(pady=20)

        # Path Analysis Frame
        self.analysis_frame = tk.Frame(self, bg="#f0f8ff", relief="ridge", bd=2)
        self.analysis_frame.pack(fill="x", padx=20, pady=5)

        self.analysis_label = tk.Label(self.analysis_frame, text="Path Analysis",
                                       font=("Helvetica", 12, 'bold'), bg="#f0f8ff")
        self.analysis_label.pack(pady=5)

        self.stats_frame = tk.Frame(self.analysis_frame, bg="#f0f8ff")
        self.stats_frame.pack(fill="x", padx=10, pady=5)

        # Stats labels
        self.max_length_label = tk.Label(self.stats_frame, text="Max Path Length: 0",
                                         font=("Helvetica", 10), bg="#f0f8ff")
        self.max_length_label.grid(row=0, column=0, sticky="w", padx=5)

        self.long_paths_label = tk.Label(self.stats_frame, text="Long Paths (>200 chars): 0",
                                         font=("Helvetica", 10), bg="#f0f8ff", fg="#ff8c00")
        self.long_paths_label.grid(row=0, column=1, sticky="w", padx=20)

        self.invalid_paths_label = tk.Label(self.stats_frame, text="Invalid Paths (>260 chars): 0",
                                            font=("Helvetica", 10), bg="#f0f8ff", fg="#dc143c")
        self.invalid_paths_label.grid(row=0, column=2, sticky="w", padx=20)

        # Top Frame for Options
        self.top_frame = tk.Frame(self, bg="#f5f5f5")
        self.top_frame.pack(pady=10)

        # Select Folder Button
        self.select_folder_button = tk.Button(self.top_frame, text="Select Folder", command=self.select_folder,
                                              font=("Helvetica", 12), bg="#4CAF50", fg="white",
                                              relief="flat", padx=20, pady=5, cursor="hand2")
        self.select_folder_button.grid(row=0, column=0, padx=10)

        # Include Hidden Folders Checkbutton
        self.include_hidden_var = tk.BooleanVar()
        self.include_hidden_check = tk.Checkbutton(self.top_frame, text="Include Hidden Folders",
                                                   variable=self.include_hidden_var,
                                                   font=("Helvetica", 10), bg="#f5f5f5")
        self.include_hidden_check.grid(row=0, column=1, padx=10)

        # Hide Node Modules Checkbutton
        self.hide_node_modules_var = tk.BooleanVar()
        self.hide_node_modules_check = tk.Checkbutton(self.top_frame, text="Hide Node Modules",
                                                      variable=self.hide_node_modules_var,
                                                      font=("Helvetica", 10), bg="#f5f5f5")
        self.hide_node_modules_check.grid(row=0, column=2, padx=10)

        # Show Path Lengths Checkbutton
        self.show_path_lengths_var = tk.BooleanVar()
        self.show_path_lengths_check = tk.Checkbutton(self.top_frame, text="Show Path Lengths",
                                                      variable=self.show_path_lengths_var,
                                                      font=("Helvetica", 10), bg="#f5f5f5")
        self.show_path_lengths_check.grid(row=0, column=3, padx=10)

        # Truncate Long Names Checkbutton
        self.truncate_names_var = tk.BooleanVar()
        self.truncate_names_check = tk.Checkbutton(self.top_frame, text="Truncate Long Names",
                                                   variable=self.truncate_names_var,
                                                   font=("Helvetica", 10), bg="#f5f5f5")
        self.truncate_names_check.grid(row=0, column=4, padx=10)

        # Save As Dropdown
        self.save_as_label = tk.Label(self.top_frame, text="Save As:", font=("Helvetica", 10), bg="#f5f5f5")
        self.save_as_label.grid(row=1, column=0, padx=5, pady=5)

        self.save_as_var = tk.StringVar(value="None")
        self.save_as_menu = ttk.Combobox(self.top_frame, textvariable=self.save_as_var, state="readonly",
                                         values=["None", "Text File", "HTML", "JSON", "Path Analysis Report"],
                                         font=("Helvetica", 10), width=20)
        self.save_as_menu.grid(row=1, column=1, padx=10, pady=5)

        # Text Widget for Folder Structure
        self.text_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=22, width=120,
                                                      font=("Courier", 9), bg="#f4f4f9", fg="#333",
                                                      bd=0, padx=10, pady=10)
        self.text_display.pack(pady=10, fill="both", expand=True)

        # Configure text tags for different path length warnings
        self.text_display.tag_configure("long_path", foreground="#ff8c00")
        self.text_display.tag_configure("invalid_path", foreground="#dc143c", background="#ffe4e1")
        self.text_display.tag_configure("normal_path", foreground="#333")

        # Search Bar
        self.search_frame = tk.Frame(self, bg="#f5f5f5")
        self.search_frame.pack(pady=5)

        self.search_label = tk.Label(self.search_frame, text="Search:", font=("Helvetica", 12), bg="#f5f5f5")
        self.search_label.pack(side="left", padx=5)

        self.search_entry = tk.Entry(self.search_frame, font=("Helvetica", 12), width=40)
        self.search_entry.pack(side="left", padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_in_structure,
                                       font=("Helvetica", 10), bg="#008CBA", fg="white",
                                       relief="flat", padx=10, pady=5)
        self.search_button.pack(side="left", padx=5)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self, bg="#f5f5f5")
        self.buttons_frame.pack(pady=10)

        # Copy to Clipboard Button
        self.copy_button = tk.Button(self.buttons_frame, text="Copy to Clipboard", command=self.copy_to_clipboard,
                                     font=("Helvetica", 12), bg="#008CBA", fg="white",
                                     relief="flat", padx=20, pady=5, cursor="hand2")
        self.copy_button.pack(side="left", padx=10)

        # Show Problems Button
        self.problems_button = tk.Button(self.buttons_frame, text="Show Path Problems", command=self.show_path_problems,
                                         font=("Helvetica", 12), bg="#dc143c", fg="white",
                                         relief="flat", padx=20, pady=5, cursor="hand2")
        self.problems_button.pack(side="left", padx=10)

        # Status Bar
        self.status_label = tk.Label(self, text="Welcome! Select a folder to get started.",
                                     font=("Helvetica", 10), bg="#f5f5f5", fg="#777")
        self.status_label.pack(side="bottom", fill="x", pady=5)

    def update_status(self, message):
        self.status_label.config(text=message)

    def truncate_name(self, name, max_length=50):
        """Truncate long file/folder names while preserving extension"""
        if len(name) <= max_length:
            return name
        
        # For files, preserve the extension
        if '.' in name and not name.startswith('.'):
            name_part, ext = os.path.splitext(name)
            if len(ext) < max_length - 10:  # Ensure we have space for meaningful truncation
                truncated_name = name_part[:max_length - len(ext) - 3] + "..."
                return truncated_name + ext
        
        # For folders or files without extension, simple truncation
        return name[:max_length - 3] + "..."

    def get_full_path_length(self, path):
        """Get the actual full path length"""
        try:
            # Use os.path.abspath to get the full absolute path
            full_path = os.path.abspath(path)
            return len(full_path)
        except:
            return len(path)

    def analyze_path(self, path):
        """Analyze path length and categorize it"""
        path_length = self.get_full_path_length(path)
        
        # Update maximum path length
        if path_length > self.max_path_length:
            self.max_path_length = path_length
        
        # Categorize paths
        if path_length > 200:
            self.long_paths.append((path, path_length))
        
        if self.is_windows and path_length > self.windows_path_limit:
            self.invalid_paths.append((path, path_length))
        
        return path_length

    def get_path_category(self, path_length):
        """Determine the category of a path based on its length"""
        if self.is_windows and path_length > self.windows_path_limit:
            return "invalid_path"
        elif path_length > 200:
            return "long_path"
        else:
            return "normal_path"

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            # Reset analysis data
            self.max_path_length = 0
            self.long_paths = []
            self.invalid_paths = []
            
            self.text_display.delete(1.0, tk.END)
            self.update_status(f"Analyzing structure of: {self.folder_path}")
            self.display_structure(self.folder_path)
            self.update_analysis_display()

    def update_analysis_display(self):
        """Update the analysis display with current statistics"""
        self.max_length_label.config(text=f"Max Path Length: {self.max_path_length}")
        self.long_paths_label.config(text=f"Long Paths (>200 chars): {len(self.long_paths)}")
        self.invalid_paths_label.config(text=f"Invalid Paths (>{self.windows_path_limit} chars): {len(self.invalid_paths)}")

    def display_structure(self, startpath):
        include_hidden = self.include_hidden_var.get()
        hide_node_modules = self.hide_node_modules_var.get()
        show_path_lengths = self.show_path_lengths_var.get()
        truncate_names = self.truncate_names_var.get()
        
        structure_output = ""
        structure_lines = []

        for root, dirs, files in os.walk(startpath):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
            if hide_node_modules:
                dirs[:] = [d for d in dirs if d.lower() != 'node_modules']

            depth = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * depth
            
            # Analyze current directory path
            current_path_length = self.analyze_path(root)
            folder_name = os.path.basename(root)
            
            if truncate_names:
                folder_name = self.truncate_name(folder_name)
            
            line_text = f"{indent}{folder_name}/"
            if show_path_lengths:
                line_text += f" [{current_path_length} chars]"
            
            line_text += "\n"
            structure_output += line_text
            
            # Store line info for coloring
            path_category = self.get_path_category(current_path_length)
            structure_lines.append((line_text, path_category))

            subindent = ' ' * 4 * (depth + 1)
            for file in files:
                file_path = os.path.join(root, file)
                file_path_length = self.analyze_path(file_path)
                
                display_name = file
                if truncate_names:
                    display_name = self.truncate_name(file)
                
                line_text = f"{subindent}{display_name}"
                if show_path_lengths:
                    line_text += f" [{file_path_length} chars]"
                
                line_text += "\n"
                structure_output += line_text
                
                # Store line info for coloring
                path_category = self.get_path_category(file_path_length)
                structure_lines.append((line_text, path_category))

        # Insert text with appropriate coloring
        current_pos = "1.0"
        for line_text, category in structure_lines:
            start_pos = current_pos
            self.text_display.insert(tk.END, line_text, category)
            # Calculate next position
            lines_added = line_text.count('\n')
            if lines_added > 0:
                current_pos = f"{float(current_pos) + lines_added}"
            else:
                current_pos = f"{current_pos}+{len(line_text)}c"

        # Handle save options
        selected_save_as = self.save_as_var.get()
        if selected_save_as == "Text File":
            self.save_to_text_file(startpath, structure_output)
        elif selected_save_as == "HTML":
            self.export_as_html(structure_output)
        elif selected_save_as == "JSON":
            self.export_as_json(structure_output)
        elif selected_save_as == "Path Analysis Report":
            self.export_path_analysis_report()

    def save_to_text_file(self, startpath, structure_output):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
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
            count = 0
            while True:
                idx = self.text_display.search(search_term, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                end_idx = f"{idx}+{len(search_term)}c"
                self.text_display.tag_add("highlight", idx, end_idx)
                self.text_display.tag_config("highlight", background="yellow", foreground="black")
                idx = end_idx
                count += 1
            self.update_status(f"Search completed for '{search_term}' - {count} matches found!")

    def show_path_problems(self):
        """Show a detailed window with path problems"""
        if not self.long_paths and not self.invalid_paths:
            messagebox.showinfo("Path Analysis", "No path length problems found!")
            return
        
        # Create a new window
        problems_window = tk.Toplevel(self)
        problems_window.title("Path Length Problems")
        problems_window.geometry("800x600")
        problems_window.configure(bg="#f5f5f5")
        
        # Title
        title_label = tk.Label(problems_window, text="Path Length Analysis Report",
                               font=("Helvetica", 16, 'bold'), bg="#f5f5f5")
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(problems_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Invalid paths tab
        if self.invalid_paths:
            invalid_frame = ttk.Frame(notebook)
            notebook.add(invalid_frame, text=f"Invalid Paths ({len(self.invalid_paths)})")
            
            invalid_text = scrolledtext.ScrolledText(invalid_frame, wrap=tk.WORD, height=20, width=90,
                                                     font=("Courier", 10))
            invalid_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            invalid_text.insert(tk.END, f"Paths exceeding Windows {self.windows_path_limit}-character limit:\n\n")
            for path, length in sorted(self.invalid_paths, key=lambda x: x[1], reverse=True):
                invalid_text.insert(tk.END, f"[{length} chars] {path}\n\n")
        
        # Long paths tab
        if self.long_paths:
            long_frame = ttk.Frame(notebook)
            notebook.add(long_frame, text=f"Long Paths ({len(self.long_paths)})")
            
            long_text = scrolledtext.ScrolledText(long_frame, wrap=tk.WORD, height=20, width=90,
                                                  font=("Courier", 10))
            long_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            long_text.insert(tk.END, "Paths longer than 200 characters:\n\n")
            for path, length in sorted(self.long_paths, key=lambda x: x[1], reverse=True):
                long_text.insert(tk.END, f"[{length} chars] {path}\n\n")

    def export_path_analysis_report(self):
        """Export a detailed path analysis report"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")])
        if not file_path:
            return
        
        report_data = {
            "analysis_date": datetime.now().isoformat(),
            "scanned_folder": getattr(self, 'folder_path', 'Unknown'),
            "max_path_length": self.max_path_length,
            "total_long_paths": len(self.long_paths),
            "total_invalid_paths": len(self.invalid_paths),
            "windows_path_limit": self.windows_path_limit,
            "long_paths": [{"path": path, "length": length} for path, length in self.long_paths],
            "invalid_paths": [{"path": path, "length": length} for path, length in self.invalid_paths]
        }
        
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("PATH LENGTH ANALYSIS REPORT\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Analysis Date: {report_data['analysis_date']}\n")
                    f.write(f"Scanned Folder: {report_data['scanned_folder']}\n")
                    f.write(f"Maximum Path Length: {report_data['max_path_length']} characters\n")
                    f.write(f"Long Paths (>200 chars): {report_data['total_long_paths']}\n")
                    f.write(f"Invalid Paths (>{self.windows_path_limit} chars): {report_data['total_invalid_paths']}\n\n")
                    
                    if self.invalid_paths:
                        f.write("INVALID PATHS (EXCEEDING WINDOWS LIMIT):\n")
                        f.write("-" * 50 + "\n")
                        for path, length in sorted(self.invalid_paths, key=lambda x: x[1], reverse=True):
                            f.write(f"[{length} chars] {path}\n")
                        f.write("\n")
                    
                    if self.long_paths:
                        f.write("LONG PATHS (>200 CHARACTERS):\n")
                        f.write("-" * 50 + "\n")
                        for path, length in sorted(self.long_paths, key=lambda x: x[1], reverse=True):
                            f.write(f"[{length} chars] {path}\n")
            
            self.update_status(f"Path analysis report saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def export_as_html(self, structure_output=None):
        if structure_output is None:
            structure_output = self.text_display.get(1.0, tk.END).strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".html",
                                                 filetypes=[("HTML files", "*.html")])
        if file_path:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Folder Structure - Version 4</title>
                <style>
                    body {{ font-family: 'Courier New', monospace; margin: 20px; }}
                    .header {{ background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
                    .long-path {{ color: #ff8c00; }}
                    .invalid-path {{ color: #dc143c; background-color: #ffe4e1; }}
                    .normal-path {{ color: #333; }}
                    pre {{ white-space: pre-wrap; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>Folder Structure Analysis - Version 4</h2>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Max Path Length: {self.max_path_length} characters</p>
                    <p>Long Paths (>200 chars): {len(self.long_paths)}</p>
                    <p>Invalid Paths (>{self.windows_path_limit} chars): {len(self.invalid_paths)}</p>
                </div>
                <pre>{structure_output}</pre>
            </body>
            </html>
            """
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.update_status(f"Folder structure exported as HTML to {file_path}")

    def export_as_json(self, structure_output=None):
        if structure_output is None:
            structure_output = self.text_display.get(1.0, tk.END).strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")])
        if file_path:
            structure_dict = {
                "folder_structure": structure_output.splitlines(),
                "analysis": {
                    "max_path_length": self.max_path_length,
                    "long_paths_count": len(self.long_paths),
                    "invalid_paths_count": len(self.invalid_paths),
                    "generated_date": datetime.now().isoformat()
                }
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(structure_dict, f, indent=4, ensure_ascii=False)
            self.update_status(f"Folder structure exported as JSON to {file_path}")

if __name__ == "__main__":
    app = FolderStructureTool()
    app.mainloop()
