# src/utils/scheduler.py
from typing import List, Tuple
from ..models.case import Case
from ..config import Config

class ScheduleCalculator:
    """Handles calculation of follow-up and strike schedules"""
    
    @staticmethod
    def calculate_next_business_day(start_day_index: int, interval: int) -> int:
        """Calculate the next business day given a starting day and interval"""
        return (start_day_index + interval) % len(Config.WEEKDAYS)

    @classmethod
    def calculate_followups(cls, case: Case) -> List[str]:
        """Calculate follow-up schedule for a case"""
        day_index = Config.WEEKDAYS.index(case.last_contact_day)
        interval = 1 if case.severity == 'B' else 2  # Adjusted for severity 'C'
        
        return [
            Config.WEEKDAYS[cls.calculate_next_business_day(day_index, (i + 1) * interval)]
            for i in range(3)  # Start from the next day after last contact
        ]

    @classmethod
    def calculate_strikes(cls, case: Case) -> Tuple[List[str], Tuple[str, str]]:
        """Calculate strike schedule and recovery period for a case"""
        day_index = Config.WEEKDAYS.index(case.last_contact_day)
        intervals = [1 if case.severity == 'B' else 2, 2, 2]
        
        # Calculate strike days
        current_index = day_index
        strike_days = []
        
        for interval in intervals:
            current_index = cls.calculate_next_business_day(current_index, interval)
            strike_days.append(Config.WEEKDAYS[current_index])
        
        # Calculate recovery period
        recovery_start = Config.WEEKDAYS[cls.calculate_next_business_day(current_index, 1)]
        recovery_end = Config.WEEKDAYS[cls.calculate_next_business_day(current_index, 2)]
        
        return strike_days, (recovery_start, recovery_end)

    @classmethod
    def format_schedule(cls, case: Case) -> str:
        """Format the schedule as a human-readable string"""
        if case.case_type == 'Follow-ups':
            followups = cls.calculate_followups(case)
            return "📅 Follow-up Schedule:\n\n" + "\n".join(
                f"Follow-up #{i+1}: {day}" 
                for i, day in enumerate(followups)
            )
        else:
            strike_days, (recovery_start, recovery_end) = cls.calculate_strikes(case)
            return (
                "⚠️ Strike Schedule:\n\n" +
                "\n".join(f"Strike #{i+1}: {day}" 
                         for i, day in enumerate(strike_days)) +
                f"\n\nRecovery Period: {recovery_start} - {recovery_end}"
            )