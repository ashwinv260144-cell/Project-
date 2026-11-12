"""Validation rules for student contact records."""

def validate_contact(name, phone, email):
    """Return (is_valid, reason) for one contact."""
    name = (name or "").strip()
    phone = (phone or "").strip()
    email = (email or "").strip()

    if not name:
        return False, "Name is blank"
    if len(phone) != 10 or not phone.isdigit() or not phone.startswith(("6", "7", "8", "9")):
        return False, "Invalid phone: must be 10 digits and start with 6, 7, 8, or 9"
    if email.count("@") != 1 or any(ch.isspace() for ch in email):
        return False, "Bad email: must contain exactly one @ and no whitespace"
    local, domain = email.split("@")
    if not local:
        return False, "Bad email: missing text before @"
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False, "Bad email: domain must contain a period not at either end"
    return True, "Valid"
