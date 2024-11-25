# Folder Structure Display Tool

## Overview
This application allows you to display the folder structure of any selected directory on your system. It provides a graphical user interface (GUI) built with **Tkinter** to easily navigate and visualize your folder contents. The tool also supports copying the folder structure to the clipboard and saving it as a text file.

### Features:
- Select a folder on your system to display its folder structure.
- Option to include hidden folders in the output.
- Copy the folder structure to the clipboard with a click of a button.
- Save the folder structure as a text file.
- Easy-to-use GUI with minimal configuration.

## Installation

### Option 1: Download the Executable (.exe)

For users who do not have Python installed, you can directly download the executable file and run it on any Windows PC.

1. Download the latest version of the `.exe` file from the [Releases](https://github.com/Arjunmehta312/show-folder-content/releases) section.
2. Double-click on the downloaded `show-folder-content.exe` to launch the application.

### Option 2: Run the Python Script

If you prefer to run the script in Python or want to modify the code, follow these instructions:

1. Clone this repository or download the source code.
   ```bash
   git clone https://github.com/Arjunmehta312/show-folder-content.git
   
2. Install the required dependencies by running the following command:
  ```bash
  pip install -r requirements.txt
  ```
Note: Make sure you have Python 3 installed on your system.

3.Run the script using:
  ```bash
python show-folder-content.py
  ```

4. Dependencies
The following Python libraries are required to run this application:

tkinter (comes pre-installed with Python)
pyperclip (for clipboard functionality)

To install pyperclip, run:
  ```bash
pip install pyperclip
```

5. Usage:
Click the "Select Folder" button to choose the directory you want to display the structure of.
Check the box to "Include hidden folders" if you want to show hidden folders.
After selecting a folder, the folder structure will be displayed in the text box.
You can click "Copy" to copy the structure to the clipboard, or use the checkbox to save the structure as a text file.

6. Troubleshooting
Missing Libraries: If you encounter errors related to missing libraries, make sure to install the required packages with pip install -r requirements.txt.
Executable Not Working: If the .exe doesn't work on your system, ensure you're running it on a Windows machine and that your system allows running unsigned executables.

7. License
This project is licensed under the MIT License - see the LICENSE file for details.

8. Contributing
Feel free to fork this project and create pull requests for improvements or bug fixes. Please ensure that your changes are well-tested before submitting them.
