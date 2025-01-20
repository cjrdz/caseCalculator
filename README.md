# Schedule Calculator Application Documentation

## Overview
The Schedule Calculator is a Python application designed to manage support cases, allowing users to add, update, delete, and view cases. The application provides a user-friendly interface built with Tkinter and ttkbootstrap, enabling users to manage case details and calculate follow-up and strike schedules based on severity levels.

## Features
- Add, update, delete, and view cases.
- Calculate follow-up and strike schedules.
- Toggle between light and dark themes.
- Verbose logging option to track actions performed in the application.

## Installation
1. Ensure you have Python 3.x installed on your machine.
2. Clone the repository or download the source code.
3. Navigate to the project directory in your terminal.
4. Install the required packages:
   ```bash
   pip install ttkbootstrap
   ```
5. Run the application:
   ```bash
   python src/main.py
   ```
## Creating an Executable

To create a standalone executable for the Schedule Calculator application, you can use the `auto-py-to-exe` package. Follow these steps:

1. Install `auto-py-to-exe`:
    ```bash
    pip install auto-py-to-exe
    ```

2. Run `auto-py-to-exe`:
    ```bash
    auto-py-to-exe
    ```

3. In the `auto-py-to-exe` interface:
    - Select `One File` and `Window Based (hide the console)`.
    - In the `Script Location` field, browse and select `src/main.py`.
    - Configure other settings as needed.

4. Click `Convert .py to .exe` to generate the executable.

The generated executable will be located in the `output` directory specified in the `auto-py-to-exe` interface.

## Usage
- Launch the application using the command above.
- Use the interface to add new cases by filling out the form and clicking "Add/Update Case."
- Select a case from the list to view its details or edit it.
- Delete cases as needed.
- Use the "Enable Verbose Logging" button to toggle logging of actions in the PowerShell.

## Main Components
- **src/main.py**: Entry point of the application. Initializes and runs the main window.
- **src/ui/main_window.py**: Contains the `MainWindow` class, which manages the main application interface and user interactions.
- **src/ui/case_details.py**: Contains the `CaseDetailsFrame` class, which handles the case details form.
- **src/ui/case_view.py**: Contains the `CaseViewDialog` class, which displays case details in a dialog.
- **src/models/case.py**: Defines the `Case` data model, representing a support case.
- **src/utils/storage.py**: Manages loading and saving cases to persistent storage (JSON file).
- **src/utils/scheduler.py**: Contains the `ScheduleCalculator` class, which calculates follow-up and strike schedules based on case details.
- **src/config.py**: Contains configuration settings for the application, such as weekdays, case types, and file paths.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or issues, please contact the project maintainer at [jonathanrdzdev@gmai.com].
