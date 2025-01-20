# src/ui/case_details.py
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ..models.case import Case
from ..config import Config

class CaseDetailsFrame(ttk.LabelFrame):
    """Frame containing the case details form"""
    
    def __init__(
        self, 
        parent: ttk.Frame,
        on_field_change: Callable,
        add_or_update_case: Callable,
        delete_case: Callable,
        **kwargs
    ):
        super().__init__(parent, text="Case Details", **kwargs)
        self.on_field_change = on_field_change
        
        self._create_form()
        self._create_buttons(add_or_update_case, delete_case)
        self._create_result_display()

    def _create_form(self) -> None:
        """Create the case details form fields"""
        # Case Number
        case_frame = ttk.Frame(self)
        case_frame.pack(fill=tk.X, pady=5)
        ttk.Label(case_frame, text="Case Number:").pack(side=tk.LEFT)
        self.case_entry = ttk.Entry(case_frame, width=20)
        self.case_entry.pack(side=tk.LEFT, padx=10)

        # Schedule Type
        type_frame = ttk.Frame(self)
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(type_frame, text="Schedule Type:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar()
        self.type_var.trace_add("write", self.on_field_change)
        
        for text in Config.CASE_TYPES:
            ttk.Radiobutton(
                type_frame,
                text=text,
                value=text,
                variable=self.type_var
            ).pack(side=tk.LEFT, padx=10)

        # Last Contact Day
        day_frame = ttk.Frame(self)
        day_frame.pack(fill=tk.X, pady=5)
        ttk.Label(day_frame, text="Last Contact Day:").pack(side=tk.LEFT)
        self.day_combobox = ttk.Combobox(
            day_frame,
            values=Config.WEEKDAYS,
            state="readonly",
            width=15
        )
        self.day_combobox.pack(side=tk.LEFT, padx=10)
        self.day_combobox.bind("<<ComboboxSelected>>", self.on_field_change)

        # Severity Level
        severity_frame = ttk.Frame(self)
        severity_frame.pack(fill=tk.X, pady=5)
        ttk.Label(severity_frame, text="Severity Level:").pack(side=tk.LEFT)
        self.severity_var = tk.StringVar()
        self.severity_var.trace_add("write", self.on_field_change)
        
        for text in Config.SEVERITY_LEVELS:
            ttk.Radiobutton(
                severity_frame,
                text=f"Severity {text}",
                value=text,
                variable=self.severity_var
            ).pack(side=tk.LEFT, padx=10)

    def _create_buttons(
        self,
        add_or_update_case: Callable,
        delete_case: Callable,
    ) -> None:
        """Create the action buttons"""
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # Use grid for better alignment
        ttk.Button(
            button_frame,
            text="Add/Update Case",
            command=add_or_update_case
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Reset",
            command=self.clear_form,
            style='danger.TButton'  # Set style to pink
        ).grid(row=0, column=1, padx=5)

    def _create_result_display(self) -> None:
        """Create the result display area"""
        self.result_text = tk.Text(
            self,
            height=10,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))

    def get_form_data(self) -> Optional[Case]:
        """Get the current form data as a Case object"""
        case_number = self.case_entry.get()
        case_type = self.type_var.get()
        day = self.day_combobox.get()
        severity = self.severity_var.get()
        
        if all([case_number, case_type, day, severity]):
            return Case(
                case_number=case_number,
                case_type=case_type,
                last_contact_day=day,
                severity=severity
            )
        return None

    def set_form_data(self, case: Case) -> None:
        """Set the form data from a Case object"""
        self.case_entry.delete(0, tk.END)
        self.case_entry.insert(0, case.case_number)
        self.type_var.set(case.case_type)
        self.day_combobox.set(case.last_contact_day)
        self.severity_var.set(case.severity)

    def show_result(self, result: str) -> None:
        """Display the calculation result"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

    def clear_form(self) -> None:
        """Clear all form fields"""
        self.case_entry.delete(0, tk.END)
        self.type_var.set('')
        self.day_combobox.set('')
        self.severity_var.set('')
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)