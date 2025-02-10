# Folder Structure Display Tool

The **Folder Structure Display Tool** is a Python-based GUI application designed to display the folder structure of any selected directory. The tool allows users to explore folder contents, search through the structure, and save the output in various formats (Text, HTML, JSON). It also provides the option to copy the structure to the clipboard.
 
## Features

- **Select Folder**: Browse and select any folder on your system.
- **Include Hidden Folders**: Option to include or exclude hidden folders in the structure display.
- **Search Functionality**: Search for specific files or folders within the displayed structure.
- **Export Options**: Save the folder structure in different formats:
  - **Text File**
  - **HTML File**
  - **JSON File**
- **Copy to Clipboard**: Copy the folder structure to the clipboard for easy sharing.
- **Modern User Interface**: Built using `Tkinter` for a clean, user-friendly experience.

## Prerequisites

To run this tool, you need to have Python 3.x installed along with the following libraries:

- `tkinter` (for the graphical user interface)
- `pyperclip` (for clipboard functionality)
- `json` (for JSON export)
- `datetime` (for timestamping)

You can install the required libraries by running:

```bash
pip install pyperclip
pip install tkinter
```
## Installation

Clone the repository:

Use git to clone the repository or download it as a ZIP file.
```bash
git clone https://github.com/Arjunmehta312/folder-display-tool.git
```
Navigate to the project directory:
```bash
cd folder-display-tool
Run the Python script:
```
To run the application, execute the show-folder-content.py script.
```bash
python python/show-folder-content.py
```
## Usage
Once the application is launched, you will see the following interface:

Select Folder: Click this button to open a file dialog where you can select a folder from your system.
Include Hidden Folders: Check this box to include hidden folders and files in the displayed structure.
Save As: Use the dropdown to select the format in which you want to save the folder structure (Text, HTML, JSON, or None).
Search: Use the search bar to find specific files or directories in the displayed structure.
Copy to Clipboard: Click this button to copy the folder structure to your clipboard.


## Versioning

#### Version 1

The first version of the tool, which displays the folder structure, allows users to copy it to the clipboard, and save it as a text file. This version provides a basic GUI without search or export options.

#### Version 2

The second version introduces additional features such as:

Search: Search for specific files/folders in the folder structure.
Export Options: Save the structure in various formats (Text, HTML, JSON).
Improved GUI: A more user-friendly layout with additional options.

#### Version 3

The third version adds more functionality and improvements:

- **Hide Node Modules**: Option to hide node_modules directories from the structure display
- **Improved UI**: Enhanced user interface with better spacing and organization
- **Bug Fixes**: Various improvements to stability and performance
- **Version Indicator**: Clear version labeling in the application title and interface

## Folder Structure
The project contains the following folder structure:

```bash
folder-display-tool/
│
├── README.md # Project documentation
├── python/ # Python scripts for different versions
│ ├── Version 1/ # Folder for version 1 of the tool
│ │ ├── Code/ # Python script for version 1
│ │ │ └── show-folder-content.py
│ │ └── Exe/ # Executable for version 1 (if applicable)
│ ├── Version 2/ # Folder for version 2 of the tool
│ │ ├── Code/ # Python script for version 2
│ │ │ └── show-folder-content.py
│ │ └── Exe/ # Executable for version 2 (if applicable)
│ └── Version 3/ # Folder for version 3 of the tool
│ ├── Code/ # Python script for version 3
│ │ └── show-folder-content.py
│ └── Exe/ # Executable for version 3 (if applicable)
```

## Contributing
Contributions are welcome! If you have any suggestions or improvements, feel free to fork the repository and submit a pull request. If you encounter any issues, please open an issue on GitHub.

## License
This project is licensed under the MIT License.
