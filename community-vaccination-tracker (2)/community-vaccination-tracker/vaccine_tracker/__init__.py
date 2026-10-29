"""Community Vaccination Tracker - a small, open-source Digital Public Good (DPG).

Modules
-------
models   : the Vaccine and Recipient classes
storage  : simple functions to add and display records in a dictionary
tracker  : the VaccinationTracker class that connects everything together
"""

from .models import DEFAULT_SCHEDULE, Recipient, Vaccine
from .storage import add_record, display_records, get_record
from .tracker import TrackerError, VaccinationTracker

__all__ = [
    "DEFAULT_SCHEDULE",
    "Recipient",
    "Vaccine",
    "add_record",
    "display_records",
    "get_record",
    "TrackerError",
    "VaccinationTracker",
]
