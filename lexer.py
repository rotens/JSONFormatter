
from constants import *


class JsonLexingException(Exception):
    pass


class Lexer:
    def __init__(self) -> None:
        self.tokens = []

    def lex(self, string):
        while len(string):
            json_string, string = self.lex_string(string)
            if json_string is not None:
                self.tokens.append(json_string)
                continue

            json_number, string = self.lex_number(string)
            if json_number is not None:
                self.tokens.append(json_number)
                continue

            json_bool, string = self.lex_bool(string)
            if json_bool is not None:
                self.tokens.append(json_bool)
                continue

            json_null, string = self.lex_null(string)
            if json_null is not None:
                self.tokens.append(None)
                continue

            if string[0] in WHITESPACE:
                string = string[1:]
            elif string[0] in JSON_SYNTAX:
                self.tokens.append(string[0])
                string = string[1:]
            else:
                raise JsonLexingException(f"Unexpected character: {string[0]}")

        return self.tokens

    def lex_string(self, string):
        json_string = ""

        if string[0] == QUOTE:
            string = string[1:]
        else:
            return None, string

        for c in string:
            if c == QUOTE:
                return json_string, string[len(json_string)+1:]
            json_string += c

        raise JsonLexingException("Expected closing quotation mark")

    def lex_number(self, string):
        json_number = ""
        number_characters = [str(d) for d in range(0, 10)] + ["-", "e", "."]

        for c in string:
            if c in number_characters:
                json_number += c
            else:
                break

        rest = string[len(json_number):]

        if not len(json_number):
            return None, string

        if "." in json_number:
            return float(json_number), rest

        return int(json_number), rest

    def lex_bool(self, string):
        string_len = len(string)

        if string_len >= 4 and string[:4] == "true":
            return True, string[4:]
        elif string_len >= 5 and string[:5] == "false":
            return False, string[5:]

        return None, string

    def lex_null(self, string):
        string_len = len(string)

        if string_len >= 4 and string[:4] == "null":
            return True, string[4]

        return None, string
