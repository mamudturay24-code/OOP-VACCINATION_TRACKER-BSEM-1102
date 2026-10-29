# Community Vaccination Tracker

A small, open-source **Python (OOP)** program that helps a community health post record
vaccine doses and see who needs a follow-up dose. It was built for **PROG211 – Object-Oriented
Programming 1** (Limkokwing University of Creative Technology, Sierra Leone) and follows
**Digital Public Goods (DPG)** principles.

> **Domain:** Health → *Vaccination Tracker*
> **Language:** Python 3.8 or newer, standard library only (nothing to install)
> **Licence:** MIT (open source)

---

## 1. The problem it solves

Paper vaccination cards get lost, and health workers can forget which children are due for the
next dose. This tool keeps a simple register, checks the dose rules (such as the minimum
number of days between doses) and shows a follow-up list.

> **Important:** the built-in vaccine schedule is **simplified for learning**. It is not medical
> advice. A real deployment must use the official national immunisation schedule.

## 2. How it follows the Digital Public Goods (DPG) principles

| DPG principle | How this project meets it |
|---|---|
| **Open-source** | Source code is public on GitHub under the MIT licence. Anyone may use, study, change and share it. |
| **Inclusive and accessible design** | Plain-language messages, numbered menu choices, clear error messages, keyboard-only use, no colours or images needed (works with screen readers), works offline on low-cost computers, no internet or account required. |
| **Privacy-respecting** | **No names, phone numbers, addresses or emails are asked for or stored.** People are identified only by an anonymous code (for example `VT-0001`) and a birth year. Data lives only in memory and disappears when the program closes. |
| **Modular and reusable** | Code is split into small modules (`models`, `storage`, `tracker`) with separate classes and functions. The `vaccine_tracker` package can be imported into other projects. Unit tests are included. |

## 3. OOP concepts used (assignment tasks)

| Task | What is implemented | Where |
|---|---|---|
| **Task 1 – Classes and objects** | `Vaccine`, `Recipient` and `VaccinationTracker` classes, each with attributes and methods. The tracker makes `Recipient` and `Vaccine` objects interact when a dose is recorded. | `vaccine_tracker/models.py`, `tracker.py` |
| **Task 2 – Data structure** | A **dictionary** (`ID → object`) stores all recipients and vaccines. Functions `add_record()` and `display_records()` add and display records. **Tuples** (optional) store dose dates and the vaccine schedule. | `vaccine_tracker/storage.py` |
| **Task 3 – Methods** | **Instance methods** (e.g. `record_dose`, `add_dose`), **class methods** (`Recipient.create`, `Vaccine.from_schedule`) and **static methods** (`Recipient.is_valid_birth_year`, `Vaccine.is_valid_name`). | `models.py`, `tracker.py` |

## 4. Project structure

```
community-vaccination-tracker/
├── README.md                 <- this file
├── LICENSE                   <- MIT licence
├── main.py                   <- interactive text menu
├── demo.py                   <- ready-made demonstration (no typing needed)
├── vaccine_tracker/
│   ├── __init__.py
│   ├── models.py             <- Vaccine and Recipient classes
│   ├── storage.py            <- add / display functions (dictionary)
│   └── tracker.py            <- VaccinationTracker class
└── tests/
    └── test_tracker.py       <- 16 unit tests
```

## 5. How to run

1. Install **Python 3.8+** from <https://www.python.org/downloads/> (check with `python --version`).
2. Download the project: `git clone https://github.com/YOUR-USERNAME/community-vaccination-tracker.git`
3. Open a terminal in the project folder and choose one:

```bash
python demo.py          # automatic demonstration
python main.py          # interactive menu
python -m unittest discover -s tests -v    # run the tests
```

(On some computers use `python3` instead of `python`.)
Optional: `python main.py --today 2026-10-06` fixes today's date, which is handy for demos.

## 6. Example usage (sample input and output)

### 6.1 Interactive menu (`python main.py --today 2026-10-06`)

Lines after a colon (such as `Choose a number: 1`) show what the user typed.
The menu is printed again after every action; it is shown only once here to save space.

```
Welcome. Your answers are kept only while this program is open.
No names, phone numbers or addresses are asked for or stored.

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
------------------------------------------
Choose a number: 1
Birth year of the person (for example 2024): 2024
Registered. This person's code is VT-0001. Write it down.

Choose a number: 2
Person's code (for example VT-0001): VT-0001
  1. BCG
  2. Pentavalent
  3. Polio (OPV)
  4. Measles-Rubella
  5. Yellow Fever
Type the number of the vaccine: 2
Date the dose was given (YYYY-MM-DD, press Enter for 2026-10-06): 2026-08-01
Saved: Pentavalent dose 1 of 3 for VT-0001 on 2026-08-01.

Choose a number: 2
Person's code (for example VT-0001): VT-0001
Type the number of the vaccine: 2
Date the dose was given (YYYY-MM-DD, press Enter for 2026-10-06): 2026-08-10
Sorry: Too early. The next Pentavalent dose can be given from 2026-08-29.

Choose a number: 2
Person's code (for example VT-0001): VT-0001
Type the number of the vaccine: 2
Date the dose was given (YYYY-MM-DD, press Enter for 2026-10-06): 2026-08-29
Saved: Pentavalent dose 2 of 3 for VT-0001 on 2026-08-29.

Choose a number: 3
Person's code: VT-0001
=== Vaccination card: VT-0001 ===
Birth year: 2024 (about 2 years old)
- Pentavalent: 2 of 3 dose(s) [2026-08-01, 2026-08-29]

Choose a number: 5
VT-0001 | Pentavalent dose 3 of 3 | from 2026-09-26 | DUE NOW

Choose a number: 0
Goodbye. Stay healthy!
```

### 6.2 Automatic demonstration (`python demo.py`)

```
##### 1. Create the tracker (it loads the default vaccines)
  - BCG: 1 dose.
  - Pentavalent: 3 doses, at least 28 days apart.
  - Polio (OPV): 4 doses, at least 28 days apart.
  - Measles-Rubella: 2 doses, at least 180 days apart.
  - Yellow Fever: 1 dose.

##### 2. Create Recipient objects (anonymous - birth year only)
  VT-0001 | born 2026 | 0 dose(s) recorded
  VT-0002 | born 2025 | 0 dose(s) recorded
  VT-0003 | born 2023 | 0 dose(s) recorded
  Total recipients created (class method): 3

##### 3. Record doses (the tracker makes Recipient and Vaccine objects interact)
  Saved: BCG dose 1 of 1 for VT-0001 on 2026-08-10.
  Saved: Pentavalent dose 1 of 3 for VT-0001 on 2026-08-25.
  Saved: Pentavalent dose 2 of 3 for VT-0001 on 2026-09-22.
  Saved: Pentavalent dose 1 of 3 for VT-0002 on 2026-08-01.
  Saved: Pentavalent dose 2 of 3 for VT-0002 on 2026-08-29.
  Saved: Measles-Rubella dose 1 of 2 for VT-0002 on 2026-03-01.
  Saved: Yellow Fever dose 1 of 1 for VT-0003 on 2026-01-15.

##### 4. Rules in action (these should be refused)
  Refused: Too early. The next Pentavalent dose can be given from 2026-10-20.
  Refused: Yellow Fever is already complete for VT-0003.
  Refused: No recipient with code 'VT-9999'. Check the code and try again.

##### 5. Vaccination card for one person
=== Vaccination card: VT-0002 ===
Birth year: 2025 (about 1 year old)
- Pentavalent: 2 of 3 dose(s) [2026-08-01, 2026-08-29]
- Measles-Rubella: 1 of 2 dose(s) [2026-03-01]

##### 6. All recipients (Task 2 display function)
  Freetown Community Health Post: 3 recipient(s), 7 dose(s) recorded.
  - VT-0001 | born 2026 | 3 dose(s) recorded
  - VT-0002 | born 2025 | 3 dose(s) recorded
  - VT-0003 | born 2023 | 1 dose(s) recorded

##### 7. Follow-up report
VT-0001 | Pentavalent dose 3 of 3 | from 2026-10-20 | not yet due
VT-0002 | Pentavalent dose 3 of 3 | from 2026-09-26 | DUE NOW
VT-0002 | Measles-Rubella dose 2 of 2 | from 2026-08-28 | DUE NOW

##### 8. Static and class methods
  Is 1850 a valid birth year? False
  Is 'BCG' a valid vaccine name? True
  Polio (OPV): 4 doses, at least 28 days apart.
```

## 7. Privacy statement

* **Data minimisation:** only a birth year and dose dates are kept – nothing that identifies a person.
* **No storage on disk and no network use:** nothing is saved or sent anywhere.
* The anonymous code must be linked to a real person *outside* the program (for example on the
  paper card), under the health post's own data-protection rules.

## 8. Limitations and ideas for the future

* Data is kept in memory only (a future version could save to a local file or database).
* The vaccine schedule is simplified; it should be replaced by the official schedule.
* Only English is supported; translations (for example into Krio) would make it more inclusive.

## 9. Contributing

Contributions are welcome. Fork the repository, make your change, run the tests, and open a pull request.

## 10. Author

**YOUR NAME** – Student ID: YOUR-ID – PROG211, Limkokwing University of Creative Technology, Sierra Leone.
Lecturer: Amandus Benjamin Coker (added as a collaborator).
