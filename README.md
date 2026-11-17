# 🗂️ File Manager Studio

A Python-based file management application built using Streamlit. It provides an interactive interface for performing CRUD (Create, Read, Update, Delete) operations on text files.

The application allows users to manage files inside a dedicated workspace directory.

## 🚀 Features

- **Create Files:** Create new text files with custom names and content.
- **Read Files:** View the contents of existing text files.
- **Update Files:** Modify existing file contents.
- **Append Content:** Add new text to existing files.
- **Overwrite Content:** Replace existing file content.
- **Rename Files:** Change file names.
- **Delete Files:** Remove unwanted files with confirmation.
- **Download Files:** Download text files to your computer.
- **Workspace Explorer:** View file names, sizes, and last modified dates.
- **Path Validation:** Restrict file operations to the application workspace.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pathlib
- Datetime

## 📁 Project Structure

```text
file-manager-studio/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── workspace/
    └── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/file-manager-studio.git
```

### 2. Navigate to the project directory

```bash
cd file-manager-studio
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows:

```powershell
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## 🔄 CRUD Operations

| Operation | Description |
|---|---|
| Create | Create a new text file |
| Read | View existing file contents |
| Update | Rename, append, or overwrite files |
| Delete | Permanently remove a selected file |

## 📂 Workspace Management

All file operations take place inside the local `workspace/` directory.

The application displays:
- File names
- File sizes
- Last modified timestamps
- Total number of files
- Total workspace storage size

## 🔒 File Safety

The application includes a path validation function to restrict user-supplied file paths to the workspace directory.

Files created by users are kept locally and are not included in the GitHub repository.

**Note:** This is a local demonstration application. It is not designed as a multi-user or production file-hosting service.

## 🎯 Learning Objectives

This project demonstrates practical implementation of:

- Python file handling
- CRUD operations
- Directory and path management
- Exception handling
- Python functions and modular programming
- Streamlit application development
- Basic file-system safety

## 🔮 Future Improvements

- Support additional file formats.
- Add search and filtering functionality.
- Add file preview for supported formats.
- Add file upload functionality.
- Improve file validation and security.
- Add file organization through folders.

## 👨‍💻 Author

Developed as a Python File Handling and CRUD project.

## 📜 License

This project is licensed under the MIT License.
