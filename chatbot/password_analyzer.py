"""Password strength analysis with real breach lookup.

Strength is estimated from length, character-class entropy and
predictable patterns. Breach checking uses the HaveIBeenPwned
Pwned Passwords range API with k-anonymity: only the first five
characters of the password's SHA-1 hash ever leave the machine.
"""
import hashlib
import math
import urllib.request

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "12345678", "111111",
    "1234567890", "letmein", "qwerty123", "admin", "welcome", "monkey",
    "dragon", "sunshine", "princess", "football", "iloveyou", "trustno1",
    "batman", "passw0rd", "master", "hello", "freedom", "whatever",
    "abc123", "shadow", "superman", "pokemon", "michael", "jordan23",
}

SEQUENCES = ("abcdefghijklmnopqrstuvwxyz", "0123456789",
             "qwertyuiop", "asdfghjkl", "zxcvbnm")

PREDICTABLE_HINTS = ("password", "passw", "qwerty", "admin", "letmein",
                     "secret", "123", "111", "000", "summer", "winter")


def _charset_size(pw: str) -> int:
    size = 0
    if any(c.islower() for c in pw):
        size += 26
    if any(c.isupper() for c in pw):
        size += 26
    if any(c.isdigit() for c in pw):
        size += 10
    if any(not c.isalnum() for c in pw):
        size += 33
    return size or 1


def _breach_count(pw: str):
    """Times the password appears in known breaches (0 if never seen,
    None if the lookup could not be completed)."""
    digest = hashlib.sha1(pw.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Sentinel-Chatbot"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            for line in resp.read().decode("utf-8").splitlines():
                hash_suffix, count = line.split(":")
                if hash_suffix == suffix:
                    return int(count)
    except Exception:
        return None
    return 0


def _has_sequence(pw: str) -> bool:
    low = pw.lower()
    for seq in SEQUENCES:
        for i in range(len(seq) - 2):
            chunk = seq[i:i + 3]
            if chunk in low or chunk[::-1] in low:
                return True
    return False


def analyze_password(pw: str) -> str:
    low = pw.lower()
    notes = []
    entropy = len(pw) * math.log2(_charset_size(pw))

    if low in COMMON_PASSWORDS:
        notes.append("This is one of the most commonly used passwords in the world.")
    if len(pw) < 12:
        notes.append("Too short — modern guidance is 12–16+ characters.")
    if _has_sequence(pw):
        notes.append("Contains a keyboard or alphabet sequence (like 'abc' or 'qwe').")
    if any(h in low for h in PREDICTABLE_HINTS):
        notes.append("Contains a predictable word or number pattern.")
    if not any(not c.isalnum() for c in pw):
        notes.append("No symbols — adding even one raises strength.")

    breaches = _breach_count(pw)
    if breaches:
        notes.append(f"Found in known breaches {breaches:,} times — never reuse this.")
    elif breaches == 0:
        notes.append("Not found in known-breach databases (good, but not a guarantee).")

    if breaches:
        verdict = "CRITICAL — change it immediately"
    elif low in COMMON_PASSWORDS or entropy < 40:
        verdict = "Weak"
    elif entropy < 60 or len(pw) < 12:
        verdict = "Fair"
    else:
        verdict = "Strong"

    tips = ("• Use a password manager with a unique password per account.\n"
            "• Passphrases beat passwords: four random words > 'P@ssw0rd!'.\n"
            "• Turn on MFA wherever it's offered.")

    lines = [f"Password strength: {verdict}",
             f"Estimated entropy: ~{int(entropy)} bits (aim for 60+).", ""]
    if notes:
        lines += [f"⚠ {n}" for n in notes] + [""]
    lines.append(tips)
    return "\n".join(lines)
