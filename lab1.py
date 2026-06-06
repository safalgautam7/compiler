KEYWORDS = {
    "int", "float", "char", "double",
    "if", "else", "while", "for",
    "return", "void"
}

DELIMITERS = {
    ";", ",", "(", ")", "{", "}", "[", "]"
}

OPERATORS = {
    "+", "-", "*", "/", "=",
    "<", ">", "!", "&", "|"
}


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"{self.value:<15} {self.token_type}"


class Tokenizer:
    def __init__(self, data):
        self.data = data
        self.position = 0

    def peek(self):
        if self.position < len(self.data):
            return self.data[self.position]
        return None

    def peek_next(self):
        if self.position + 1 < len(self.data):
            return self.data[self.position + 1]
        return None

    def advance(self):
        if self.position >= len(self.data):
            return None

        ch = self.data[self.position]
        self.position += 1
        return ch

    def skip_whitespace(self):
        while self.peek() is not None and self.peek().isspace():
            self.advance()

    def skip_comment(self):
        while self.peek() is not None and self.peek() != '\n':
            self.advance()

    def read_identifier(self):
        identifier = ""

        while (
            self.peek() is not None and
            (self.peek().isalnum() or self.peek() == "_")
        ):
            identifier += self.advance()

        return identifier

    def read_number(self):
        number = ""
        decimal_found = False

        while self.peek() is not None:
            ch = self.peek()

            if ch.isdigit():
                number += self.advance()
            elif ch == "." and not decimal_found:
                decimal_found = True
                number += self.advance()
            else:
                break

        return number

    def read_string(self):
        string_literal = ""

        self.advance()  # opening quote
        while self.peek() is not None and self.peek() != '"':
            string_literal += self.advance()

        if self.peek() == '"':
            self.advance()  # closing quote

        return string_literal

    def read_operator(self):
        ch = self.peek()
        if ch not in OPERATORS:
            return None

        next_ch = self.peek_next()
        two_char_ops = {
            "==", "!=", "<=", ">=",
            "&&", "||",
            "++", "--",
            "+=", "-=", "*=", "/="
        }

        if (
            next_ch is not None and
            ch + next_ch in two_char_ops
        ):
            return self.advance() + self.advance()

        return self.advance()

    def next_token(self):
        while True:
            self.skip_whitespace()

            ch = self.peek()

            if ch is None:
                return None

            # skip single-line comments
            if ch == "/" and self.peek_next() == "/":
                self.advance()
                self.advance()
                self.skip_comment()
                continue

            break

        if ch.isalpha() or ch == "_":
            identifier = self.read_identifier()

            if identifier in KEYWORDS:
                return Token("KEYWORD", identifier)

            return Token("IDENTIFIER", identifier)

        if ch.isdigit():
            return Token("NUMBER", self.read_number())

        if ch == '"':
            return Token("STRING", self.read_string())

        if ch in DELIMITERS:
            self.advance()
            return Token("DELIMITER", ch)

        if ch in OPERATORS:
            return Token("OPERATOR", self.read_operator())

        self.advance()
        return Token("SYMBOL", ch)

    def tokenize(self):
        tokens = []

        while True:
            token = self.next_token()

            if token is None:
                break

            tokens.append(token)

        return tokens


def main():
    try:
        with open("input.txt", "r") as f:
            data = f.read()
    except FileNotFoundError:
        print("input.txt not found")
        return

    tokenizer = Tokenizer(data)

    print(f"{'LEXEME':<15} TOKEN")

    for token in tokenizer.tokenize():
        print(token)


if __name__ == "__main__":
    main()