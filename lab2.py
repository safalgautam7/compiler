def match(pattern, text):
    return match_here(pattern, text)


def match_here(pattern, text):
    if not pattern:
        return text == ""

    if len(pattern) > 1:
        if pattern[1] == '*':
            return match_star(pattern[0], pattern[2:], text)

        if pattern[1] == '+':
            return match_plus(pattern[0], pattern[2:], text)

        if pattern[1] == '?':
            return match_question(pattern[0], pattern[2:], text)

    if text and (pattern[0] == text[0] or pattern[0] == '.'):
        return match_here(pattern[1:], text[1:])

    return False


def match_star(ch, remaining_pattern, text):
    if match_here(remaining_pattern, text):
        return True

    i = 0
    while i < len(text) and (text[i] == ch or ch == '.'):
        if match_here(remaining_pattern, text[i + 1:]):
            return True
        i += 1

    return False


def match_plus(ch, remaining_pattern, text):
    if not text:
        return False

    if text[0] != ch and ch != '.':
        return False

    return match_star(ch, remaining_pattern, text[1:])


def match_question(ch, remaining_pattern, text):
    if match_here(remaining_pattern, text):
        return True

    if text and (text[0] == ch or ch == '.'):
        return match_here(remaining_pattern, text[1:])

    return False


def main():
    try:
        with open("lab2_input.txt", "r") as file:
            lines = file.readlines()

        print(f"{'PATTERN':<15}{'STRING':<15}RESULT")

        for line in lines:
            line = line.strip()

            if not line:
                continue

            pattern, string = line.split(maxsplit=1)

            if match(pattern, string):
                result = "Valid"
            else:
                result = "Invalid"

            print(f"{pattern:<15}{string:<15}{result}")

    except FileNotFoundError:
        print("input.txt not found")


if __name__ == "__main__":
    main()