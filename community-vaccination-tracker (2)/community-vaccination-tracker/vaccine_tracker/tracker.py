"""tracker.py - VaccinationTracker connects Vaccine and Recipient objects.

This class is the 'manager'. It holds two dictionaries (vaccines and recipients)
and makes the objects work together, for example when a dose is recorded.
"""

from datetime import date

from .models import DEFAULT_SCHEDULE, Recipient, Vaccine
from .storage import add_record, display_records


class TrackerError(ValueError):
    """A problem the user can fix. The message is written in plain language."""


class VaccinationTracker:
    """Records vaccinations for anonymous recipients at one health post."""

    def __init__(self, facility="Community Health Post"):
        self.facility = facility
        self._vaccines = {}    # dictionary: vaccine name -> Vaccine object
        self._recipients = {}  # dictionary: recipient ID -> Recipient object

    @classmethod
    def with_default_vaccines(cls, facility="Community Health Post"):
        """Create a tracker that already knows the default vaccines."""
        tracker = cls(facility)
        for name in DEFAULT_SCHEDULE:
            tracker.add_vaccine(Vaccine.from_schedule(name))
        return tracker

    # ---- setting up -----------------------------------------------------------
    def add_vaccine(self, vaccine):
        add_record(self._vaccines, vaccine.name, vaccine)

    def vaccine_names(self):
        """Tuple of all vaccine names."""
        return tuple(self._vaccines)

    def register_recipient(self, birth_year):
        """Create a new anonymous recipient and store it."""
        try:
            recipient = Recipient.create(birth_year)
        except ValueError as problem:
            raise TrackerError(str(problem)) from problem
        add_record(self._recipients, recipient.recipient_id, recipient)
        return recipient

    # ---- finding objects --------------------------------------------------------
    def get_recipient(self, recipient_id):
        key = str(recipient_id).strip().upper()
        if key not in self._recipients:
            raise TrackerError(f"No recipient with code '{recipient_id}'. Check the code and try again.")
        return self._recipients[key]

    def get_vaccine(self, vaccine_name):
        for name, vaccine in self._vaccines.items():
            if name.lower() == str(vaccine_name).strip().lower():
                return vaccine
        raise TrackerError(f"Unknown vaccine '{vaccine_name}'.")

    # ---- the main action: objects interacting -----------------------------------
    def record_dose(self, recipient_id, vaccine_name, dose_date=None, today=None):
        """Record one dose after checking the rules. Returns a friendly message."""
        today = today or date.today()
        dose_date = dose_date or today
        recipient = self.get_recipient(recipient_id)   # a Recipient object
        vaccine = self.get_vaccine(vaccine_name)       # a Vaccine object

        if dose_date > today:
            raise TrackerError("The dose date cannot be in the future.")
        if dose_date.year < recipient.birth_year:
            raise TrackerError("The dose date is before the birth year.")

        taken = recipient.doses_of(vaccine.name)
        if vaccine.is_complete(taken):
            raise TrackerError(f"{vaccine.name} is already complete for {recipient.recipient_id}.")
        earliest = vaccine.next_dose_date(taken)
        if earliest and dose_date < earliest:
            raise TrackerError(f"Too early. The next {vaccine.name} dose can be given from {earliest}.")

        recipient.add_dose(vaccine.name, dose_date)    # Recipient changes itself
        number = len(recipient.doses_of(vaccine.name))
        return (f"Saved: {vaccine.name} dose {number} of {vaccine.doses_required} "
                f"for {recipient.recipient_id} on {dose_date}.")

    # ---- reports ----------------------------------------------------------------
    def vaccination_card(self, recipient_id, today=None):
        """Text card showing everything recorded for one recipient."""
        today = today or date.today()
        recipient = self.get_recipient(recipient_id)
        lines = (
            f"=== Vaccination card: {recipient.recipient_id} ===",
            f"Birth year: {recipient.birth_year} ({recipient.age_text(today)})",
        )
        text = "\n".join(lines)
        if not recipient.total_doses():
            return text + "\nNo doses recorded yet."
        details = "\n".join(
            f"- {name}: {len(dates)} of {self.get_vaccine(name).doses_required} dose(s) "
            f"[{', '.join(str(d) for d in dates)}]"
            for name, dates in recipient.dose_history()
        )
        return text + "\n" + details

    def _due_lines(self, today):
        """Generate one text line per follow-up dose (a generator, no list needed)."""
        for recipient in self._recipients.values():
            for name, dates in recipient.dose_history():
                vaccine = self.get_vaccine(name)
                nxt = vaccine.next_dose_date(dates)
                if nxt is None:
                    continue
                status = "DUE NOW" if nxt <= today else "not yet due"
                yield (f"{recipient.recipient_id} | {name} dose {len(dates) + 1} of "
                       f"{vaccine.doses_required} | from {nxt} | {status}")

    def due_report(self, today=None):
        """Text report of recipients whose next dose is due or coming up."""
        today = today or date.today()
        text = "\n".join(self._due_lines(today))
        return text or "No follow-up doses are waiting."

    def summary(self):
        """One-line summary of the whole register."""
        total = sum(r.total_doses() for r in self._recipients.values())
        return (f"{self.facility}: {len(self._recipients)} recipient(s), "
                f"{total} dose(s) recorded.")

    def show_all_recipients(self):
        """Print every recipient using the Task 2 display function."""
        display_records(self._recipients, "No recipients registered yet.")

    def show_all_vaccines(self):
        """Print every vaccine using the Task 2 display function."""
        display_records(self._vaccines, "No vaccines loaded.")
