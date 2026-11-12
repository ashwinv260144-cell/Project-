# Student Registration & Contact Intelligence System

**Semester 1 BCA – Python Programming Final Project**

A command-line application that imports student contacts from CSV, validates records, filters duplicates, supports student record management, and prints basic business intelligence reports. It uses only the Python standard library.

## Requirements
- Python 3.8 or later
- No third-party packages and no SQL database required

## Project files
```text
student_registration/
├── contacts.csv              # Raw sample input (20 records)
├── students_clean.csv        # Generated clean output
├── validator.py              # Name, phone and email validation
├── loader.py                 # CSV ingestion and duplicate filtering
├── analytics.py              # BI report generation
├── main.py                   # Interactive management menu
├── proof/
│   ├── console_output.txt    # Sample run / ingestion evidence
│   └── test_cases.txt        # Validation test evidence
└── README.md
```

## Validation rules
- Name must not be blank after trimming whitespace.
- Phone must contain exactly 10 digits and start with 6, 7, 8 or 9.
- Email must contain exactly one `@`, no whitespace, a non-empty local part, and a domain containing a period that is not at the beginning or end.
- A phone number or email already accepted from an earlier row is treated as a duplicate.

## How to run
Open a terminal in this folder.

1. Process the raw CSV and create `students_clean.csv`:
   ```bash
   python loader.py
   ```
2. Start the interactive application:
   ```bash
   python main.py
   ```
3. Generate the standalone analytics report:
   ```bash
   python analytics.py
   ```

The menu supports viewing, searching, registering, updating and deleting records. Choose option 7 to save and exit.

## Analytics
The report shows total processed, accepted and rejected rows, acceptance percentage, rejection categories, phone-prefix counts (9/8/7/6), and email-domain counts.

## Important note about the PDF sample
The PDF's preview states 20 total, 13 valid and 7 rejected. Applying the exact validation and duplicate rules in the PDF to the 20 CSV rows printed in that same PDF produces **12 accepted and 8 rejected**. This project follows the stated validation rules and actual row data rather than hard-coding the preview totals. Rejection categories in the report are calculated from the actual processing result.

## Testing
Run:
```bash
python -m unittest discover -s proof -p "test_*.py" -v
```
See `proof/test_cases.txt` and `proof/console_output.txt` for included evidence.
