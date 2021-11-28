from constants import *


class JsonParsingException(Exception):
    pass


class Parser:
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
            if type(t) in (str, int, float, bool) and t not in JSON_SYNTAX:
                return True
            return False

        if t == OPENBRACE and tokens[-1] == CLOSEBRACE:
            brace = 0
            for i, token in enumerate(tokens):
                if token == OPENBRACE:
                    brace += 1
                if token == CLOSEBRACE:
                    brace -= 1
                if brace == 0 and i != len(tokens)-1:
                    return False
            if brace == 0:
                return True
            return False

        if t == OPENBRACKET and tokens[-1] == CLOSEBRACKET:
            bracket = 0
            for i, token in enumerate(tokens):
                if token == OPENBRACKET:
                    bracket += 1
                if token == CLOSEBRACKET:
                    bracket -= 1
                if bracket == 0 and i != len(tokens)-1:
                    return False
            if bracket == 0:
                return True
            return False

        return False

    def parse_array(self, tokens):
        t = tokens[0]
        if t == CLOSEBRACKET:
            return tokens[1:]

        while True:
            tokens = self.parse(tokens)

            t = self.get_token(tokens)
            if t == CLOSEBRACKET:
                return tokens[1:]
            elif t is None:
                raise JsonParsingException('Expected closing bracket')
            elif t != COMMA:
                raise JsonParsingException('Expected comma after array\'s element')
            
            tokens = tokens[1:]
            if tokens[0] == CLOSEBRACKET or tokens[0] == CLOSEBRACE:
                raise JsonParsingException('Expected array\'s element after comma')

    def parse_object(self, tokens):
        t = tokens[0]
        if t == CLOSEBRACE:
            return tokens[1:]

        while True:
            json_key = tokens[0]
            if type(json_key) is str and json_key not in JSON_SYNTAX:
                tokens = tokens[1:]
            else:
                raise JsonParsingException(f'Expected string key, got: {json_key}')

            if tokens[0] != COLON:
                raise JsonParsingException(
                    f'Expected colon after key in object, got: {json_key}')
            
            tokens = tokens[1:]
            if tokens[0] == CLOSEBRACE or tokens[0] == CLOSEBRACKET:
                raise JsonParsingException('Expected value after colon in object')

            tokens = self.parse(tokens)

            t = self.get_token(tokens)
            if t == CLOSEBRACE:
                return tokens[1:]
            elif t is None:
                raise JsonParsingException('Expected closing brace')
            elif t != COMMA:
                raise JsonParsingException(
                    f'Expected comma or closing brace after pair in object, got: {t}')
            
            tokens = tokens[1:]
            if tokens[0] == CLOSEBRACE or tokens[0] == CLOSEBRACKET:
                raise JsonParsingException('Expected key after comma in object')
    
    def get_token(self, tokens):
        try:
            return tokens[0]
        except IndexError:
            return None
