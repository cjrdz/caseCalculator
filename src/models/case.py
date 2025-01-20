# src/models/case.py
from dataclasses import dataclass
from typing import Literal, Dict, Any

CaseType = Literal['Follow-ups', 'Strikes']
SeverityLevel = Literal['B', 'C']

@dataclass
class Case:
    """Represents a support case with its scheduling information"""
    case_number: str
    case_type: CaseType
    last_contact_day: str
    severity: SeverityLevel
    
    @property
    def unique_id(self) -> str:
        """Create a unique identifier that combines case number and type"""
        return f"{self.case_number}_{self.case_type}"

    @classmethod
    def from_dict(cls, case_number: str, data: Dict[str, Any]) -> 'Case':
        """Create a Case instance from a dictionary"""
        return cls(
            case_number=case_number,
            case_type=data['type'],
            last_contact_day=data['day'],
            severity=data['severity']
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Case instance to a dictionary"""
        return {
            'type': self.case_type,
            'day': self.last_contact_day,
            'severity': self.severity
        }

    def __str__(self) -> str:
        return f"Case {self.case_number} ({self.case_type})"