# Cutie Browser

Cutie Browser is a simple, lightweight web browser built with Python and the PyQt5 library. It provides a basic tabbed browsing experience.

## Features

*   Tabbed browsing
    *   Enhanced tab management:
        *   Dedicated 'New Tab' (+) button.
        *   Tabs are closable with an 'x' button.
        *   Tab titles now display the actual web page title for better identification.
*   Navigation controls:
    *   Back, Forward, and Refresh buttons for web page navigation.
    *   Home button to quickly navigate to a default homepage.
*   Navigation controls:
    *   Back, Forward, and Refresh buttons for web page navigation.
*   URL navigation with defaulting to HTTPS
*   Basic error handling for page loads
*   File downloads
*   "About" dialog

## Prerequisites

*   Python 3.x
*   pip (Python package installer)

## Setup and Running

1.  **Clone the repository (or download the files):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the browser:**
    ```bash
    python CutieBrowser.py
    ```

## Building an Executable

You can package Cutie Browser into a standalone executable using PyInstaller. This allows users to run the browser without needing to install Python or the required dependencies.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Package the application:**

    *   **For a single file executable (simpler distribution, potentially slower startup):**
        ```bash
        pyinstaller --onefile --windowed --name CutieBrowser CutieBrowser.py
        ```
    *   **For a one-folder bundle (faster startup, results in a folder with multiple files):**
        ```bash
        # pyinstaller --windowed --name CutieBrowser CutieBrowser.py
        ```
        (Note: The one-folder command is often just `pyinstaller --windowed CutieBrowser.py` if the name matches the script, but `--name` can be explicit.)

### Troubleshooting & Considerations

*   **Platform Specificity:** An executable built on one OS (e.g., Windows) will only run on that OS. You'll need to build separately for Windows, macOS, and Linux.
*   **File Size:** Executables including PyQtWebEngine can be quite large due to the bundled browser engine.
*   **PyQtWebEngine Issues:** Packaging PyQtWebEngine can sometimes be complex. If the application doesn't start or browser functionality is broken after packaging, you might need to:
    *   Examine PyInstaller's build warnings in the console for clues.
    *   Manually specify paths to QtWebEngine components using PyInstaller's `--add-binary` option (or `--add-data` for non-binary files) or by modifying the `.spec` file. This is often necessary to ensure all required Qt plugins and processes are included. For example, you might need to include `QtWebEngineProcess` or specific Qt plugins. An illustrative (and might need adjustment based on your OS and environment) command could look like:
        ```bash
        # Example for Windows: Adjust paths based on your environment (esp. venv location)
        # You may need to find the exact location of these files in your PyQt5 installation.
        pyinstaller --onefile --windowed --name CutieBrowser \
          --add-binary="path/to/your/venv/Lib/site-packages/PyQt5/Qt5/bin/QtWebEngineProcess.exe:." \
          --add-binary="path/to/your/venv/Lib/site-packages/PyQt5/Qt5/resources:resources" \
          --add-binary="path/to/your/venv/Lib/site-packages/PyQt5/Qt5/translations:translations" \
          --add-binary="path/to/your/venv/Lib/site-packages/PyQt5/Qt5/plugins/platforms:platforms" \
          --add-binary="path/to/your/venv/Lib/site-packages/PyQt5/Qt5/plugins/imageformats:imageformats" \
          --add-binary="path/to/your/venv/Lib/site-packages/PyQt5/Qt5/plugins/webenginewidgets:webenginewidgets" \
          CutieBrowser.py
        ```
    *   Replace `path/to/your/venv` with the actual path to your virtual environment's `site-packages` directory, or the global site-packages directory if not using a virtual environment. The exact paths and required Qt components (like DLLs, .so files, or .dylib files) can vary significantly between operating systems and PyQt5 versions. Consult PyInstaller and PyQt documentation for advanced troubleshooting and specifics for your OS.
*   **Spec File:** For more complex scenarios or fine-grained control, you can first generate a `.spec` file (`pyi-makespec CutieBrowser.py`) and then edit it to include specific hooks, binaries, or data files before building with PyInstaller (`pyinstaller CutieBrowser.spec`).

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Ensure your changes are well-documented and, if applicable, include tests.
5.  Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
