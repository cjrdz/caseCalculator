# src/config.py
class Config:
    """Application configuration settings"""
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    CASE_TYPES = ['Follow-ups', 'Strikes']
    SEVERITY_LEVELS = ['B', 'C']
    DEFAULT_THEME = "solar"
    DEFAULT_WINDOW_SIZE = "1200x800"
    CASES_FILE = "data/cases.json"