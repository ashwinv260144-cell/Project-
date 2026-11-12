"""Business intelligence reports using core Python."""
from collections import Counter
from loader import ingest

def build_report(students, total_processed=None, rejected=None):
    rejected = rejected or []
    total = total_processed if total_processed is not None else len(students)
    prefixes = Counter(s["phone"][0] for s in students if s.get("phone"))
    domains = Counter(s["email"].rsplit("@", 1)[-1].lower() for s in students if "@" in s.get("email", ""))
    reasons = Counter()
    for item in rejected:
        reason = item["reason"].lower()
        if "phone" in reason:
            reasons["Invalid Phone / Missing Phone"] += 1
        elif "email" in reason:
            reasons["Bad Email"] += 1
        elif "name" in reason:
            reasons["Missing Name"] += 1
        else:
            reasons["Other / Duplicate"] += 1
    accuracy = (len(students) / total * 100) if total else 0.0
    return {"total": total, "accepted": len(students), "rejected": len(rejected),
            "accuracy": accuracy, "prefixes": prefixes, "domains": domains, "reasons": reasons}

def print_report(report):
    line = "=" * 62
    print("\\n" + line)
    print("       STUDENT REGISTRATION - BUSINESS INTELLIGENCE")
    print(line)
    print(f"Total Contacts Processed : {report['total']}")
    print(f"Valid Registrations      : {report['accepted']}")
    print(f"Rejected Records         : {report['rejected']}")
    print(f"Data Quality Accuracy   : {report['accuracy']:.1f}%")
    print("\\n--- Rejection Diagnostics ---")
    if report["reasons"]:
        for reason, count in report["reasons"].most_common():
            print(f"{reason:<30}: {count}")
    else:
        print("No rejected records in this report.")
    print("\\n--- Telecom Network Breakdown ---")
    for digit in "9876":
        print(f"{digit}-Series{' ':>23}: {report['prefixes'].get(digit, 0)} students")
    print("\\n--- Email Domain Breakdown ---")
    for domain, count in report["domains"].most_common():
        print(f"@{domain:<25}: {count} students")
    print(line)

def run_analytics():
    result = ingest(verbose=False)
    print_report(build_report(result["students"], result["total"], result["rejected"]))

if __name__ == "__main__":
    run_analytics()
