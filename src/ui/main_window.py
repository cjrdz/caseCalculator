# src/ui/main_window.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ..models.case import Case
from ..config import Config
from ..utils.storage import StorageManager
from ..utils.scheduler import ScheduleCalculator
from .case_list import CaseListFrame
from .case_details import CaseDetailsFrame
from .case_view import CaseViewDialog

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        # Initialize the dark theme flag
        self.is_dark = True  # Set initial theme to dark
        
        # Check if StorageManager.load_cases() is functioning correctly
        self.cases = StorageManager.load_cases()  # Ensure this does not raise an error
        
        # Ensure tb.Window is initialized correctly
        self.root = tb.Window(themename=Config.DEFAULT_THEME)  # Check Config.DEFAULT_THEME
        
        self.root.title("Schedule Calculator")
        self.root.geometry("1200x800")
        
        self._create_theme_toggle()
        self._create_main_frame()
        
        # Set the initial theme correctly
        self.root.style.theme_use("solar")  # Set initial theme to dark
        self.theme_button.config(text="🌙 Light Theme")  # Set the button text correctly

    def _create_theme_toggle(self) -> None:
        """Create the theme toggle button"""
        self.theme_button = ttk.Button(
            self.root,
            text="🌙 Light Theme",
            command=self._toggle_theme,
            style='primary-outline.TButton'
        )
        self.theme_button.pack(anchor='ne', padx=20, pady=10)

    def _create_main_frame(self) -> None:
        """Create the main application frame"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Display frame
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.case_list = CaseListFrame(
            display_frame,
            on_case_select=self._on_case_select,
            view_case_callback=self._view_case,
            edit_case=self._edit_case,
            delete_cases=self._delete_cases
        )
        self.case_list.pack(fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right side - Details frame
        self.case_details = CaseDetailsFrame(
            main_frame,
            on_field_change=self._on_field_change,
            add_or_update_case=self._add_or_update_case,
            delete_case=self._delete_case
        )
        self.case_details.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Initialize the case list
        self.case_list.refresh_case_list(self.cases)

    def _toggle_theme(self) -> None:
        """Toggle between light and dark themes"""
        self.is_dark = not self.is_dark
        new_theme = "solar" if self.is_dark else "litera"
        self.root.style.theme_use(new_theme)
        self.theme_button.config(
            text="🌙 Light Theme" if self.is_dark else "🌑 Dark Mode"
        )
        self.root.update_idletasks()  # Ensure the UI updates immediately

    def _on_case_select(self) -> None:
        """Handle case selection from the list"""
        case_number, case_type = self.case_list.get_selected_case()
        if case_number and case_type:
            case = self.cases[case_type][case_number]
            self.case_details.set_form_data(case)
            self._calculate_schedule()

    def _on_field_change(self, *args) -> None:
        """Handle form field changes"""
        case = self.case_details.get_form_data()
        if case:
            self._calculate_schedule()

    def _calculate_schedule(self) -> None:
        """Calculate and display the schedule"""
        case = self.case_details.get_form_data()
        if case:
            schedule = ScheduleCalculator.format_schedule(case)
            self.case_details.show_result(schedule)

    def _add_or_update_case(self) -> None:
        """Add or update a case in storage"""
        case = self.case_details.get_form_data()
        if case:
            unique_id = case.unique_id
            self.cases[case.case_type][unique_id] = case
            StorageManager.save_cases(self.cases)
            self.case_list.refresh_case_list(self.cases)
            self.case_details.clear_form()

    def _delete_case(self, case: Case) -> None:
        """Delete a case from storage"""
        unique_id = case.unique_id
        if case.case_type in self.cases and unique_id in self.cases[case.case_type]:
            del self.cases[case.case_type][unique_id]
            StorageManager.save_cases(self.cases)
            self.case_list.refresh_case_list(self.cases)
            self.case_details.clear_form()

    def _view_case(self, selected_case: tuple[str, str]) -> None:
        """Open the case view dialog for the selected case"""
        case_number, case_type = selected_case  # Unpack the tuple
        if case_number and case_type:
            # Find the case using the unique_id
            unique_id = f"{case_number}_{case_type}"
            case = self.cases[case_type].get(unique_id)
            if case:
                CaseViewDialog(
                    self.root,
                    case,
                    self._edit_case
                )

    def _edit_case(self, case: Case) -> None:
        """Handle editing a case"""
        self.case_details.set_form_data(case)
        self._calculate_schedule()

    def _delete_cases(self, selected_cases: list[tuple[str, str]]) -> None:
        """Delete multiple cases from storage"""
        for case_number, case_type in selected_cases:
            unique_id = f"{case_number}_{case_type}"
            if case_type in self.cases and unique_id in self.cases[case_type]:
                del self.cases[case_type][unique_id]
        
        StorageManager.save_cases(self.cases)
        self.case_list.refresh_case_list(self.cases)
        self.case_details.clear_form()

    def _show_message(self, message: str) -> None:
        """Show a message to the user"""
        print(message)  # In a production app, you might want to use a proper message box

    def run(self) -> None:
        """Start the application"""
        self.root.mainloop()