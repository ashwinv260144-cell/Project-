"""Menu-driven student registration and contact management application."""
import csv
from pathlib import Path
from loader import ingest, CLEAN_FILE, FIELDS
from validator import validate_contact
from analytics import build_report, print_report

def load_students():
    if not CLEAN_FILE.exists():
        ingest(verbose=False)
    with open(CLEAN_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_students(students):
    # Reassign sequential IDs before saving.
    for index, student in enumerate(students, start=1):
        student["id"] = str(index)
    with open(CLEAN_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)

def show_students(students):
    if not students:
        print("No student records found."); return
    print("\\n{:<5} {:<22} {:<12} {}".format("ID", "NAME", "PHONE", "EMAIL"))
    print("-" * 75)
    for s in students:
        print("{:<5} {:<22} {:<12} {}".format(s["id"], s["name"][:21], s["phone"], s["email"]))

def search_students(students):
    term = input("Enter phone, email or name: ").strip().lower()
    matches = [s for s in students if term in s["phone"].lower() or term in s["email"].lower() or term in s["name"].lower()]
    show_students(matches)

def register_student(students):
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip().lower()
    ok, reason = validate_contact(name, phone, email)
    if not ok:
        print("Registration rejected:", reason); return
    if any(s["phone"] == phone or s["email"].lower() == email for s in students):
        print("Registration rejected: duplicate phone or email."); return
    students.append({"id": str(len(students)+1), "name": name, "phone": phone, "email": email})
    save_students(students)
    print("Student registered successfully.")

def update_student(students):
    key = input("Enter student ID or phone to update: ").strip()
    student = next((s for s in students if s["id"] == key or s["phone"] == key), None)
    if not student:
        print("Student not found."); return
    name = input(f"Name [{student['name']}]: ").strip() or student["name"]
    phone = input(f"Phone [{student['phone']}]: ").strip() or student["phone"]
    email = input(f"Email [{student['email']}]: ").strip().lower() or student["email"]
    ok, reason = validate_contact(name, phone, email)
    if not ok:
        print("Update rejected:", reason); return
    for other in students:
        if other is not student and (other["phone"] == phone or other["email"].lower() == email):
            print("Update rejected: duplicate phone or email."); return
    student.update(name=name, phone=phone, email=email)
    save_students(students)
    print("Student updated successfully.")

def delete_student(students):
    key = input("Enter student ID or phone to delete: ").strip()
    student = next((s for s in students if s["id"] == key or s["phone"] == key), None)
    if not student:
        print("Student not found."); return
    confirm = input(f"Delete {student['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student); save_students(students); print("Student deleted.")
    else:
        print("Delete cancelled.")

def show_analytics():
    result = ingest(verbose=False)
    print_report(build_report(result["students"], result["total"], result["rejected"]))

def main():
    students = load_students()
    while True:
        print("\\n===== STUDENT REGISTRATION SYSTEM =====")
        print("1. View All Students")
        print("2. Search Record")
        print("3. Register Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Analytics Report")
        print("7. Exit")
        choice = input("Choose an option (1-7): ").strip()
        if choice == "1": show_students(students)
        elif choice == "2": search_students(students)
        elif choice == "3": register_student(students)
        elif choice == "4": update_student(students)
        elif choice == "5": delete_student(students)
        elif choice == "6": show_analytics()
        elif choice == "7":
            save_students(students); print("Records saved. Goodbye!"); break
        else: print("Invalid option. Please choose 1 to 7.")

if __name__ == "__main__":
    main()
