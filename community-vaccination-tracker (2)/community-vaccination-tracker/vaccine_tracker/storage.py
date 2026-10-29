"""storage.py - simple functions to ADD and DISPLAY records (Task 2).

The data structure used is a DICTIONARY:
    key   = a unique ID (for example "VT-0001")
    value = an object (a Recipient or a Vaccine)
A dictionary is a good choice because we can find any record instantly by its ID.
"""


def add_record(store, key, record):
    """Add a record to the dictionary. Refuses duplicate IDs."""
    if key in store:
        raise ValueError(f"A record with ID '{key}' already exists.")
    store[key] = record
    return record


def get_record(store, key):
    """Find one record by its ID. Raises KeyError if it does not exist."""
    return store[key]


def display_records(store, empty_message="No records yet."):
    """Print every record in the dictionary, one per line (each record shows its own ID)."""
    if not store:
        print(empty_message)
        return
    for record in store.values():  # loop through the dictionary
        print(f"  - {record}")
