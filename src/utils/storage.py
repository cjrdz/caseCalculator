# src/utils/storage.py
import json
import os
from typing import Dict
from ..models.case import Case
from ..config import Config

class StorageManager:
    """Handles saving and loading cases from persistent storage"""
    
    @staticmethod
    def load_cases() -> Dict[str, Dict[str, Case]]:
        """Load cases from the JSON file and convert them to Case objects"""
        cases: Dict[str, Dict[str, Case]] = {
            "Follow-ups": {},
            "Strikes": {}
        }
        
        if os.path.exists(Config.CASES_FILE):
            with open(Config.CASES_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                
                for case_type in Config.CASE_TYPES:
                    for case_number, case_data in data.get(case_type, {}).items():
                        # Create case instance
                        case = Case.from_dict(
                            case_number=case_number,
                            data=case_data
                        )
                        # Store using unique_id as the key
                        cases[case_type][case.unique_id] = case
        
        return cases

    @staticmethod
    def save_cases(cases: Dict[str, Dict[str, Case]]) -> None:
        """Save cases to the JSON file"""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(Config.CASES_FILE), exist_ok=True)
        
        # Convert cases to dictionary format
        data = {
            case_type: {
                case.case_number: case.to_dict()  # Use case_number for storage
                for case in case_dict.values()
            }
            for case_type, case_dict in cases.items()
        }
        
        # Save to file
        with open(Config.CASES_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)