from constants import *


class JsonParsingException(Exception):
    pass


class Parser:
    def __init__(self) -> None:
        self.test = ""

    def parse(self, tokens, is_root=False):
        if is_root and not self.parse_root(tokens):
            raise JsonParsingException('Root element not valid')

        t = tokens[0]

        if t == OPENBRACKET:
            return self.parse_array(tokens[1:])
        elif t == OPENBRACE:
            return self.parse_object(tokens[1:])
        else:
            return tokens[1:]

    def parse_root(self, tokens):
        t = tokens[0]

        if len(tokens) == 1:
            if t is None:
                return True 
            if type(t) in (str, int, float, bool):
                return True
            return False

        if t == OPENBRACE and tokens[-1] == CLOSEBRACE:
            return True
        if t == OPENBRACKET and tokens[-1] == CLOSEBRACKET:
            return True

        return False


    def parse_array(self, tokens):
        t = tokens[0]
        if t == CLOSEBRACKET:
            return tokens[1:]

        while True:
            tokens = self.parse(tokens)

            t = tokens[0]
            if t == CLOSEBRACKET:
                return tokens[1:]
            elif t != COMMA:
                raise JsonParsingException('Expected comma after array\'s element')
            else:
                tokens = tokens[1:]

        # raise JsonParsingException('Expected closing array bracket')

    
    def parse_object(self, tokens):
        t = tokens[0]
        if t == CLOSEBRACE:
            return tokens[1:]

        while True:
            json_key = tokens[0]
            if type(json_key) is str:
                tokens = tokens[1:]
            else:
                raise JsonParsingException(f'Expected string key, got: {json_key}')

            if tokens[0] != COLON:
                raise JsonParsingException(f'Expected colon after key in object, got: {json_key}')

            tokens = self.parse(tokens[1:])

            t = tokens[0]
            if t == CLOSEBRACE:
                return tokens[1:]
            elif t != COMMA:
                raise JsonParsingException(f'Expected comma after pair in object, got: {json_key}')

            tokens = tokens[1:]

        # raise JsonParsingException('Expected end-of-object bracket')

    # def parse(self, tokens, is_root=False):
    #     if is_root and not self.parse_root(tokens):
    #         raise JsonParsingException('Root element not valid')

    #     t = tokens[0]

    #     if t == OPENBRACKET:
    #         return self.parse_array(tokens[1:])
    #     elif t == OPENBRACE:
    #         return self.parse_object(tokens[1:])
    #     else:
    #         return t, tokens[1:]

    # def parse_root(self, tokens):
    #     t = tokens[0]

    #     if len(tokens) == 1:
    #         if t is None:
    #             return True 
    #         if type(t) in (str, int, float, bool):
    #             return True
    #         return False

    #     if t == OPENBRACE and tokens[-1] == CLOSEBRACE:
    #         return True
    #     if t == OPENBRACKET and tokens[-1] == CLOSEBRACKET:
    #         return True

    #     return False


    # def parse_array(self, tokens):
    #     json_array = []

    #     t = tokens[0]
    #     if t == CLOSEBRACKET:
    #         return json_array, tokens[1:]

    #     while True:
    #         json, tokens = self.parse(tokens)
    #         json_array.append(json)

    #         t = tokens[0]
    #         if t == CLOSEBRACKET:
    #             return json_array, tokens[1:]
    #         elif t != COMMA:
    #             raise JsonParsingException('Expected comma after array\'s element')
    #         else:
    #             tokens = tokens[1:]

    #     # raise JsonParsingException('Expected closing array bracket')

    
    # def parse_object(self, tokens):
    #     json_object = {}

    #     t = tokens[0]
    #     if t == CLOSEBRACE:
    #         return json_object, tokens[1:]

    #     while True:
    #         json_key = tokens[0]
    #         if type(json_key) is str:
    #             tokens = tokens[1:]
    #         else:
    #             raise JsonParsingException(f'Expected string key, got: {json_key}')

    #         if tokens[0] != COLON:
    #             raise JsonParsingException(f'Expected colon after key in object, got: {json_key}')

    #         json_value, tokens = self.parse(tokens[1:])

    #         json_object[json_key] = json_value

    #         t = tokens[0]
    #         if t == CLOSEBRACE:
    #             return json_object, tokens[1:]
    #         elif t != COMMA:
    #             raise JsonParsingException(f'Expected comma after pair in object, got: {json_key}')

    #         tokens = tokens[1:]

    #     # raise JsonParsingException('Expected end-of-object bracket')