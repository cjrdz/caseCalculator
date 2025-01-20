# src/ui/case_list.py
import tkinter as tk
from tkinter import ttk
from ttkbootstrap.dialogs import Messagebox
from typing import Callable, Dict
from ..models.case import Case

class CaseListFrame(ttk.LabelFrame):
    """Frame containing the case list with search functionality"""
    
    def __init__(
        self, 
        parent: ttk.Frame,
        on_case_select: Callable,
        view_case_callback: Callable,
        edit_case: Callable,
        delete_cases: Callable,
        **kwargs
    ):
        super().__init__(parent, text="Cases", **kwargs)
        self.parent = parent  # This should be the MainWindow instance
        self.on_case_select = on_case_select
        self.view_case = view_case_callback  # This should be a method that accepts selected_case
        self.edit_case = edit_case
        self.delete_cases = delete_cases
        
        self._create_search_frame()
        self._create_notebook()
        
    def _create_search_frame(self) -> None:
        """Create the search frame with search entry and buttons"""
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=(10,0))
        
        # Left side - Search
        left_frame = ttk.Frame(search_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(left_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(left_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,10))
        self.search_entry.bind('<KeyRelease>', self._on_search)
        
        # Right side - Buttons
        right_frame = ttk.Frame(search_frame)
        right_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            right_frame, 
            text="View Selected",
            command=self._view_selected,
            style='primary.TButton'
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            right_frame, 
            text="Delete Selected",
            command=self._delete_selected,
            style='danger.TButton'
        ).pack(side=tk.LEFT, padx=2)

    def _create_notebook(self) -> None:
        """Create notebook with separate tabs for follow-ups and strikes"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frames for each tab
        followup_frame = ttk.Frame(self.notebook)
        strike_frame = ttk.Frame(self.notebook)
        
        # Create listboxes with improved styling and multi-select
        self.followup_listbox = tk.Listbox(
            followup_frame, 
            height=20,
            selectmode=tk.EXTENDED,  # Changed to allow multi-select
            activestyle='none',
            font=('TkDefaultFont', 10),
            borderwidth=0,
            highlightthickness=1
        )
        self.followup_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.strike_listbox = tk.Listbox(
            strike_frame, 
            height=20,
            selectmode=tk.EXTENDED,  # Changed to allow multi-select
            activestyle='none',
            font=('TkDefaultFont', 10),
            borderwidth=0,
            highlightthickness=1
        )
        self.strike_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind events
        self.followup_listbox.bind('<Double-Button-1>', self._on_double_click)
        self.strike_listbox.bind('<Double-Button-1>', self._on_double_click)
        
        # Add frames to notebook
        self.notebook.add(followup_frame, text="Follow-ups")
        self.notebook.add(strike_frame, text="Strikes")

    def refresh_case_list(self, cases: Dict[str, Dict[str, Case]]) -> None:
        """Refresh the case lists with current data"""
        self.followup_listbox.delete(0, tk.END)
        self.strike_listbox.delete(0, tk.END)
        
        # Show unique case numbers for each type
        for case in cases["Follow-ups"].values():
            self.followup_listbox.insert(tk.END, case.case_number)
            
        for case in cases["Strikes"].values():
            self.strike_listbox.insert(tk.END, case.case_number)

    def _on_search(self) -> None:
        """Handle search functionality"""
        search_term = self.search_entry.get().lower()
        current_tab = self.notebook.select()
        listbox = (
            self.followup_listbox 
            if "followup" in str(current_tab) 
            else self.strike_listbox
        )
        
        listbox.delete(0, tk.END)
        for item in self._get_all_items(listbox):
            if search_term in item.lower():
                listbox.insert(tk.END, item)

    def _get_all_items(self, listbox: tk.Listbox) -> list:
        """Get all items from a listbox"""
        return [listbox.get(i) for i in range(listbox.size())]

    def get_selected_case(self) -> tuple[str, str]:
        """Get the currently selected case number and type"""
        current_tab = self.notebook.index(self.notebook.select())
        listbox = (
            self.followup_listbox 
            if current_tab == 0 
            else self.strike_listbox
        )
        case_type = Config.CASE_TYPES[current_tab]
        
        selection = listbox.curselection()
        if not selection:
            return None, None
            
        case_number = listbox.get(selection[0])
        return case_number, case_type

    def _on_double_click(self, event) -> None:
        """Handle double-click on a case in the list"""
        selected_case = self.get_selected_case()
        if selected_case:
            self.view_case(selected_case)

    def get_selected_cases(self) -> list[tuple[str, str]]:
        """Get all selected cases numbers and types"""
        current_tab = self.notebook.index(self.notebook.select())
        listbox = self.followup_listbox if current_tab == 0 else self.strike_listbox
        case_type = Config.CASE_TYPES[current_tab]
        
        selected_indices = listbox.curselection()
        return [(listbox.get(idx), case_type) for idx in selected_indices]

    def _view_selected(self) -> None:
        """View the selected cases"""
        selected_cases = self.get_selected_cases()  # Get all selected cases
        for selected_case in selected_cases:
            self.view_case(selected_case)  # Call view_case for each selected case

    def _delete_selected(self) -> None:
        """Delete all selected cases with custom styled confirmation dialog"""
        selected_cases = self.get_selected_cases()
        if selected_cases:
            if len(selected_cases) == 1:
                title = "Delete Case"
                msg = (
                    f"Are you sure you want to delete case "
                    f"'{selected_cases[0][0]}'?\n\n"
                    "This action cannot be undone."
                )
            else:
                title = "Delete Multiple Cases"
                msg = (
                    f"Are you sure you want to delete these "
                    f"{len(selected_cases)} cases?\n\n"
                    "This action cannot be undone."
                )
            
            # Create custom messagebox
            dialog = Messagebox.show_question(
                title=title,
                message=msg,
                alert=True,
                parent=self,
                buttons=['Yes:primary', 'Cancel:secondary']
            )
            
            if dialog == 'Yes':
                self.delete_cases(selected_cases)
                # Show success message
                Messagebox.show_info(
                    title="Success",
                    message=(
                        "Successfully deleted "
                        f"{len(selected_cases)} case{'s' if len(selected_cases) > 1 else ''}"
                    ),
                    parent=self
                )
                
# src/ui/case_details.py
from tkinter import ttk
from typing import Optional
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
        delete_case: Callable
    ) -> None:
        """Create the action buttons"""
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Add/Update Case",
            command=add_or_update_case
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Delete Case",
            command=delete_case
        ).pack(side=tk.LEFT, padx=5)

    def _create_result_display(self) -> None:
        """Create the result display area"""
        self.result_text = tk.Text(
            self,
            height=10,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

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