import re


def check_rules(text):
    violations = []
    slope = re.search(r'1:(\d+)', text)
    width = re.search(r'(\d+)\s*inches', text)

    if slope and int(slope.group(1)) > 12:
        violations.append("Slope too steep")
    if width and int(width.group(1)) < 36:
        violations.append("Width too narrow")
    if "handrail" not in text.lower():
        violations.append("Handrails not mentioned")

    return violations


if __name__ == "__main__":
    sample_text = """
    Ramp slope: 1:10
    Ramp width: 30 inches
    Handrails: only one side
    """
    print(check_rules(sample_text))
