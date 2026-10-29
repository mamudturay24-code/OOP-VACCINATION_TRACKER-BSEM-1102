"""main.py - simple text menu for the Community Vaccination Tracker.

Run:  python main.py
Optional: python main.py --today 2026-10-06   (fixes today's date, useful for demos)

Designed to be easy to use: plain words, numbered choices, helpful error messages,
keyboard only, no colours or images, and it works offline on any computer with Python.
"""

import argparse
from datetime import date

from vaccine_tracker import TrackerError, VaccinationTracker

MENU = """
------------------------------------------
 COMMUNITY VACCINATION TRACKER
------------------------------------------
 1. Register a new person
 2. Record a vaccine dose
 3. Show one person's vaccination card
 4. Show everyone registered
 5. Who needs a follow-up dose?
 6. Show the vaccine list
 0. Exit
------------------------------------------"""


def ask_date(prompt, default):
    """Ask for a date as YYYY-MM-DD. Pressing Enter gives the default date."""
    text = input(f"{prompt} (YYYY-MM-DD, press Enter for {default}): ").strip()
    if not text:
        return default
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise TrackerError("That date is not valid. Use the form 2026-10-06.")


def ask_birth_year():
    text = input("Birth year of the person (for example 2024): ").strip()
    if not text.isdigit():
        raise TrackerError("Please type the birth year using numbers only.")
    return int(text)


def choose_vaccine(tracker):
    """Show numbered vaccines and return the chosen name."""
    choices = {str(n): name for n, name in enumerate(tracker.vaccine_names(), start=1)}
    for number, name in choices.items():
        print(f"  {number}. {name}")
    pick = input("Type the number of the vaccine: ").strip()
    if pick not in choices:
        raise TrackerError("Please choose one of the numbers shown.")
    return choices[pick]


def run(today):
    tracker = VaccinationTracker.with_default_vaccines()
    print("Welcome. Your answers are kept only while this program is open.")
    print("No names, phone numbers or addresses are asked for or stored.")
    while True:
        print(MENU)
        try:
            choice = input("Choose a number: ").strip()
        except EOFError:
            break
        try:
            if choice == "1":
                person = tracker.register_recipient(ask_birth_year())
                print(f"Registered. This person's code is {person.recipient_id}. Write it down.")
            elif choice == "2":
                code = input("Person's code (for example VT-0001): ")
                vaccine = choose_vaccine(tracker)
                when = ask_date("Date the dose was given", today)
                print(tracker.record_dose(code, vaccine, when, today))
            elif choice == "3":
                print(tracker.vaccination_card(input("Person's code: "), today))
            elif choice == "4":
                print(tracker.summary())
                tracker.show_all_recipients()
            elif choice == "5":
                print(tracker.due_report(today))
            elif choice == "6":
                tracker.show_all_vaccines()
            elif choice == "0":
                print("Goodbye. Stay healthy!")
                break
            else:
                print("Please choose a number from the menu.")
        except TrackerError as problem:
            print(f"Sorry: {problem}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Community Vaccination Tracker")
    parser.add_argument("--today", help="fix today's date as YYYY-MM-DD (for demos and testing)")
    args = parser.parse_args()
    run(date.fromisoformat(args.today) if args.today else date.today())
