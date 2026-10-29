"""models.py - the two core classes of the Vaccination Tracker.

Vaccine   : describes ONE vaccine (name, number of doses, days between doses).
Recipient : an ANONYMOUS person who receives vaccines.
            No name, phone number or address is ever stored (privacy by design).

Only dictionaries and tuples are used as data structures in this project.
"""

from datetime import date, timedelta

# A simplified schedule for learning purposes only (NOT medical advice).
# Each value is a TUPLE: (doses_required, days_between_doses).
# Tuples cannot be changed, so the schedule cannot be altered by accident.
DEFAULT_SCHEDULE = {
    "BCG": (1, 0),
    "Pentavalent": (3, 28),
    "Polio (OPV)": (4, 28),
    "Measles-Rubella": (2, 180),
    "Yellow Fever": (1, 0),
}


class Vaccine:
    """One type of vaccine and the rules for giving it."""

    def __init__(self, name, doses_required, interval_days=0):
        if not Vaccine.is_valid_name(name):
            raise ValueError("Vaccine name must be 2 to 40 letters, numbers, spaces, - or ().")
        if doses_required < 1:
            raise ValueError("A vaccine needs at least 1 dose.")
        if interval_days < 0:
            raise ValueError("Days between doses cannot be negative.")
        self.name = name.strip()
        self.doses_required = doses_required
        self.interval_days = interval_days

    # ---- class method: an alternative way to create an object -------------
    @classmethod
    def from_schedule(cls, name):
        """Build a Vaccine from the built-in DEFAULT_SCHEDULE."""
        if name not in DEFAULT_SCHEDULE:
            raise ValueError(f"'{name}' is not in the default schedule.")
        doses, interval = DEFAULT_SCHEDULE[name]
        return cls(name, doses, interval)

    # ---- static method: a helper that needs no object ----------------------
    @staticmethod
    def is_valid_name(name):
        """True if the name is 2-40 characters of letters, numbers, space, - ( )."""
        if not isinstance(name, str):
            return False
        text = name.strip()
        allowed = all(ch.isalnum() or ch in " -()" for ch in text)
        return 2 <= len(text) <= 40 and allowed

    # ---- instance methods: they work on ONE vaccine object ----------------
    def is_complete(self, doses_taken):
        """True when the person has had all required doses."""
        return len(doses_taken) >= self.doses_required

    def next_dose_date(self, doses_taken):
        """Earliest date for the next dose, or None if complete / not started."""
        if self.is_complete(doses_taken) or not doses_taken:
            return None
        return doses_taken[-1] + timedelta(days=self.interval_days)

    def describe(self):
        """Plain-language description of this vaccine."""
        if self.doses_required == 1:
            return f"{self.name}: 1 dose."
        return (f"{self.name}: {self.doses_required} doses, "
                f"at least {self.interval_days} days apart.")

    def __str__(self):
        return self.describe()


class Recipient:
    """An anonymous person who receives vaccines (identified only by a code)."""

    _counter = 0  # CLASS attribute: shared by every Recipient object

    def __init__(self, recipient_id, birth_year):
        if not Recipient.is_valid_birth_year(birth_year):
            raise ValueError("Birth year must be a whole number from 1900 to this year.")
        self.recipient_id = recipient_id
        self.birth_year = birth_year
        # dictionary: vaccine name -> TUPLE of dates when doses were given
        self._doses = {}

    # ---- class methods ------------------------------------------------------
    @classmethod
    def create(cls, birth_year):
        """Create a Recipient with an automatic anonymous code such as VT-0001."""
        next_number = cls._counter + 1
        recipient = cls(f"VT-{next_number:04d}", birth_year)  # raises if invalid
        cls._counter = next_number  # only counted if creation worked
        return recipient

    @classmethod
    def total_created(cls):
        """How many recipients have been created so far."""
        return cls._counter

    # ---- static method ------------------------------------------------------
    @staticmethod
    def is_valid_birth_year(year, current_year=None):
        """True for a whole-number year between 1900 and the current year."""
        current = current_year if current_year is not None else date.today().year
        return isinstance(year, int) and 1900 <= year <= current

    # ---- instance methods ---------------------------------------------------
    def age(self, today=None):
        """Approximate age in years (birth year only, so it is approximate)."""
        today = today or date.today()
        return today.year - self.birth_year

    def age_text(self, today=None):
        """Age in friendly words, for example 'about 1 year old'."""
        years = self.age(today)
        if years <= 0:
            return "under 1 year old"
        return f"about {years} year{'s' if years != 1 else ''} old"

    def add_dose(self, vaccine_name, dose_date):
        """Save one dose. A new tuple is built because tuples cannot change."""
        self._doses[vaccine_name] = self._doses.get(vaccine_name, ()) + (dose_date,)

    def doses_of(self, vaccine_name):
        """Tuple of dates for one vaccine (empty tuple if none yet)."""
        return self._doses.get(vaccine_name, ())

    def dose_history(self):
        """(vaccine name, tuple of dates) pairs for every vaccine started."""
        return self._doses.items()

    def total_doses(self):
        """Total number of doses this person has received."""
        return sum(len(dates) for dates in self._doses.values())

    def __str__(self):
        return (f"{self.recipient_id} | born {self.birth_year} | "
                f"{self.total_doses()} dose(s) recorded")
