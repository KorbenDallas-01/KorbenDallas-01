"""
password_generator.py
----------------------
Generate secure passwords and check the strength of any password.

Usage:
    python password_generator.py generate                   # default 16 chars
    python password_generator.py generate --length 24
    python password_generator.py generate --no-symbols
    python password_generator.py generate --no-digits
    python password_generator.py check "MyP@ssw0rd!"
"""

import argparse
import re
import secrets
import string


# ── Constants ──────────────────────────────────────────────────────────────────

LOWERCASE  = string.ascii_lowercase
UPPERCASE  = string.ascii_uppercase
DIGITS     = string.digits
SYMBOLS    = "!@#$%^&*()-_=+[]{}|;:,.<>?"

# Common weak passwords to flag immediately
COMMON_PASSWORDS = {
    "password", "123456", "password123", "qwerty", "abc123",
    "letmein", "monkey", "iloveyou", "admin", "welcome",
}


# ── Password generation ────────────────────────────────────────────────────────

def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length:       Total length of the password (minimum 4).
        use_uppercase: Include uppercase letters.
        use_digits:   Include digits.
        use_symbols:  Include special characters.

    Returns:
        A randomly generated password string.

    Raises:
        ValueError: If length is below 4 or no character sets are selected.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    alphabet = LOWERCASE
    required_chars: list[str] = [secrets.choice(LOWERCASE)]

    if use_uppercase:
        alphabet += UPPERCASE
        required_chars.append(secrets.choice(UPPERCASE))

    if use_digits:
        alphabet += DIGITS
        required_chars.append(secrets.choice(DIGITS))

    if use_symbols:
        alphabet += SYMBOLS
        required_chars.append(secrets.choice(SYMBOLS))

    if not alphabet:
        raise ValueError("At least one character set must be selected.")

    # Fill remaining characters randomly, then shuffle
    remaining = [secrets.choice(alphabet) for _ in range(length - len(required_chars))]
    password_chars = required_chars + remaining

    # Shuffle using secrets-safe method (Fisher-Yates via secrets.SystemRandom)
    rng = secrets.SystemRandom()
    rng.shuffle(password_chars)

    return "".join(password_chars)


# ── Strength checking ──────────────────────────────────────────────────────────

def check_strength(password: str) -> dict:
    """
    Analyse the strength of a password and return a detailed report.

    Args:
        password: The password string to evaluate.

    Returns:
        A dict with keys: score (0–100), label, and a list of feedback strings.
    """
    feedback: list[str] = []
    score = 0

    # Immediate disqualifiers
    if password.lower() in COMMON_PASSWORDS:
        return {
            "score": 0,
            "label": "Very Weak",
            "feedback": ["❌ This is one of the most common passwords. Change it immediately."],
        }

    # Length scoring
    length = len(password)
    if length >= 20:
        score += 30
    elif length >= 16:
        score += 25
    elif length >= 12:
        score += 20
    elif length >= 8:
        score += 10
        feedback.append("⚠️  Consider using at least 12 characters.")
    else:
        score += 0
        feedback.append("❌ Password is too short (minimum 8 characters recommended).")

    # Character variety scoring
    has_lower   = bool(re.search(r"[a-z]", password))
    has_upper   = bool(re.search(r"[A-Z]", password))
    has_digit   = bool(re.search(r"\d", password))
    has_symbol  = bool(re.search(r"[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]", password))

    variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
    score += variety_count * 15

    if not has_lower:
        feedback.append("💡 Add lowercase letters.")
    if not has_upper:
        feedback.append("💡 Add uppercase letters.")
    if not has_digit:
        feedback.append("💡 Add digits (0–9).")
    if not has_symbol:
        feedback.append("💡 Add special characters (!@#$ etc.).")

    # Penalise repetition
    if re.search(r"(.)\1{2,}", password):
        score -= 10
        feedback.append("⚠️  Avoid repeating the same character 3+ times in a row.")

    # Penalise sequential patterns
    sequences = ["abcdef", "qwerty", "123456", "654321"]
    for seq in sequences:
        if seq in password.lower():
            score -= 10
            feedback.append(f"⚠️  Avoid predictable sequences like '{seq}'.")
            break

    score = max(0, min(score, 100))

    if score >= 80:
        label = "Strong 💪"
    elif score >= 60:
        label = "Moderate 🔶"
    elif score >= 30:
        label = "Weak 🔴"
    else:
        label = "Very Weak ☠️"

    if not feedback:
        feedback.append("✅ Looks good!")

    return {"score": score, "label": label, "feedback": feedback}


def print_strength_report(password: str) -> None:
    """Print a formatted strength report for a given password."""
    result = check_strength(password)
    bar_filled = int(result["score"] / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    print(f"\nPassword : {'*' * len(password)}  ({len(password)} chars)")
    print(f"Strength : {result['label']}")
    print(f"Score    : [{bar}] {result['score']}/100")
    print("\nFeedback:")
    for line in result["feedback"]:
        print(f"  {line}")
    print()


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate secure passwords and check password strength."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate subcommand
    gen = subparsers.add_parser("generate", help="Generate a new password")
    gen.add_argument("--length", type=int, default=16, help="Password length (default: 16)")
    gen.add_argument("--no-uppercase", action="store_true", help="Exclude uppercase letters")
    gen.add_argument("--no-digits",    action="store_true", help="Exclude digits")
    gen.add_argument("--no-symbols",   action="store_true", help="Exclude special characters")

    # check subcommand
    chk = subparsers.add_parser("check", help="Check the strength of a password")
    chk.add_argument("password", type=str, help="The password to evaluate")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "generate":
        try:
            password = generate_password(
                length=args.length,
                use_uppercase=not args.no_uppercase,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
            )
            print(f"\n✅ Generated password:\n\n  {password}\n")
            print_strength_report(password)
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "check":
        print_strength_report(args.password)


if __name__ == "__main__":
    main()
