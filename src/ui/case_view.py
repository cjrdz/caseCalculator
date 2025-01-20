# src/ui/case_view.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ..models.case import Case
from ..utils.scheduler import ScheduleCalculator
from typing import Callable

class CaseViewDialog:
    """Dialog window for viewing case details"""
    
    def __init__(self, parent: tk.Tk, case: Case, edit_callback: Callable = None):
        self.popup = tb.Toplevel(parent)
        self.parent = parent
        self.case = case
        self.edit_callback = edit_callback
        
        self.popup.title(f"Case Details - {case.case_number}")
        self.popup.geometry("400x600")
        
        # Make the window resizable
        self.popup.resizable(True, True)
        
        # Configure grid weights for dynamic resizing
        self.popup.grid_columnconfigure(0, weight=1)
        self.popup.grid_rowconfigure(0, weight=1)
        
        self._create_content(case)
        
    def _create_content(self, case: Case) -> None:
        """Create the dialog content"""
        # Main container with grid
        content = ttk.Frame(self.popup, padding="20")
        content.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(4, weight=1)  # Make schedule frame expandable
        
        # Case details - using grid instead of pack
        ttk.Label(
            content,
            text=f"Case Number: {case.case_number}",
            font=("", 12, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(5,15))
        
        ttk.Label(
            content,
            text=f"Type: {case.case_type}",
            font=("", 10)
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        ttk.Label(
            content,
            text=f"Last Contact Day: {case.last_contact_day}",
            font=("", 10)
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        ttk.Label(
            content,
            text=f"Severity Level: {case.severity}",
            font=("", 10)
        ).grid(row=3, column=0, sticky="w", pady=5)
        
        # Schedule frame
        schedule_frame = ttk.LabelFrame(content, text="Schedule", padding="10")
        schedule_frame.grid(row=4, column=0, sticky="nsew", pady=(20,10))
        
        # Configure schedule frame grid
        schedule_frame.grid_columnconfigure(0, weight=1)
        schedule_frame.grid_rowconfigure(0, weight=1)
        
        # Schedule text widget
        schedule_text = tk.Text(
            schedule_frame, 
            wrap=tk.WORD,
            font=('TkDefaultFont', 10),
            padx=10,
            pady=10
        )
        schedule_text.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical", command=schedule_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        schedule_text.configure(yscrollcommand=scrollbar.set)
        
        # Calculate and display schedule
        schedule = ScheduleCalculator.format_schedule(case)
        schedule_text.insert("1.0", schedule)
        schedule_text.config(state=tk.DISABLED)
        
        # Button frame at the bottom
        button_frame = ttk.Frame(content)
        button_frame.grid(row=5, column=0, sticky="ew", pady=(10,0))
        
        # Configure button frame columns
        button_frame.grid_columnconfigure(0, weight=1)  # Center spacing
        button_frame.grid_columnconfigure(1, weight=1)  # Center spacing

        # Edit button
        if self.edit_callback:
            ttk.Button(
                button_frame,
                text="Edit",
                command=self._edit_case,
                style='info.TButton',
                width=15
            ).grid(row=0, column=0, padx=5)

        # Close button
        ttk.Button(
            button_frame,
            text="Close",
            command=self.popup.destroy,
            style='danger.TButton',  # Set style to pink
            width=15
        ).grid(row=0, column=1, padx=5)

    def _edit_case(self):
        """Handle edit case action"""
        if self.edit_callback:
            self.edit_callback(self.case)
            self.popup.destroy()