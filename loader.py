"""CSV ingestion, validation, duplicate prevention and clean-file export."""
import csv
from pathlib import Path
from validator import validate_contact

ROOT = Path(__file__).resolve().parent
RAW_FILE = ROOT / "contacts.csv"
CLEAN_FILE = ROOT / "students_clean.csv"
FIELDS = ["id", "name", "phone", "email"]

def ingest(raw_file=RAW_FILE, clean_file=CLEAN_FILE, verbose=True):
    students, seen_phones, seen_emails, rejected = [], set(), set(), []
    total = 0
    with open(raw_file, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        for row_number, row in enumerate(reader, start=2):
            total += 1
            name = (row.get("name") or "").strip()
            phone = (row.get("phone") or "").strip()
            email = (row.get("email") or "").strip().lower()
            ok, reason = validate_contact(name, phone, email)
            if not ok:
                rejected.append({"row": row_number, "name": name, "reason": reason})
                continue
            if phone in seen_phones:
                rejected.append({"row": row_number, "name": name, "reason": f"Duplicate phone: {phone}"})
                continue
            if email in seen_emails:
                rejected.append({"row": row_number, "name": name, "reason": f"Duplicate email: {email}"})
                continue
            seen_phones.add(phone)
            seen_emails.add(email)
            students.append({"id": str(len(students) + 1), "name": name, "phone": phone, "email": email})

    with open(clean_file, "w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)

    result = {"total": total, "accepted": len(students), "rejected": rejected, "students": students}
    if verbose:
        print_ingestion_log(result)
    return result

def print_ingestion_log(result):
    print("\\n=== CSV INGESTION LOG ===")
    print(f"Total rows read : {result['total']}")
    print(f"Valid accepted  : {result['accepted']}")
    print(f"Rejected rows   : {len(result['rejected'])}")
    for item in result["rejected"]:
        print(f"Row {item['row']}: {item['name'] or '[blank name]'} - {item['reason']}")

if __name__ == "__main__":
    ingest()
