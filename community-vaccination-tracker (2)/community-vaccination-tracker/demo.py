"""demo.py - a ready-made demonstration (no typing needed).

Run:  python demo.py
It creates objects, makes them interact, and prints the results.
"""

from datetime import date

from vaccine_tracker import Recipient, TrackerError, Vaccine, VaccinationTracker

TODAY = date(2026, 10, 6)  # fixed date so the output is always the same


def heading(text):
    print(f"\n##### {text}")


def main():
    heading("1. Create the tracker (it loads the default vaccines)")
    tracker = VaccinationTracker.with_default_vaccines("Freetown Community Health Post")
    tracker.show_all_vaccines()

    heading("2. Create Recipient objects (anonymous - birth year only)")
    ama = tracker.register_recipient(2026)
    kofi = tracker.register_recipient(2025)
    zainab = tracker.register_recipient(2023)
    for person in (ama, kofi, zainab):
        print(" ", person)
    print("  Total recipients created (class method):", Recipient.total_created())

    heading("3. Record doses (the tracker makes Recipient and Vaccine objects interact)")
    plan = (
        (ama.recipient_id, "BCG", date(2026, 8, 10)),
        (ama.recipient_id, "Pentavalent", date(2026, 8, 25)),
        (ama.recipient_id, "Pentavalent", date(2026, 9, 22)),
        (kofi.recipient_id, "Pentavalent", date(2026, 8, 1)),
        (kofi.recipient_id, "Pentavalent", date(2026, 8, 29)),
        (kofi.recipient_id, "Measles-Rubella", date(2026, 3, 1)),
        (zainab.recipient_id, "Yellow Fever", date(2026, 1, 15)),
    )
    for code, vaccine, when in plan:
        print(" ", tracker.record_dose(code, vaccine, when, TODAY))

    heading("4. Rules in action (these should be refused)")
    attempts = (
        (ama.recipient_id, "Pentavalent", date(2026, 10, 6)),   # too early
        (zainab.recipient_id, "Yellow Fever", date(2026, 10, 1)),  # already complete
        ("VT-9999", "BCG", date(2026, 10, 1)),                  # unknown person
    )
    for code, vaccine, when in attempts:
        try:
            tracker.record_dose(code, vaccine, when, TODAY)
        except TrackerError as problem:
            print("  Refused:", problem)

    heading("5. Vaccination card for one person")
    print(tracker.vaccination_card(kofi.recipient_id, TODAY))

    heading("6. All recipients (Task 2 display function)")
    print(" ", tracker.summary())
    tracker.show_all_recipients()

    heading("7. Follow-up report")
    print(tracker.due_report(TODAY))

    heading("8. Static and class methods")
    print("  Is 1850 a valid birth year?", Recipient.is_valid_birth_year(1850, 2026))
    print("  Is 'BCG' a valid vaccine name?", Vaccine.is_valid_name("BCG"))
    new_vaccine = Vaccine.from_schedule("Polio (OPV)")
    print(" ", new_vaccine.describe())


if __name__ == "__main__":
    main()
