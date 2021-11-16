from lexer import Lexer, JsonLexingException
from parser_ import Parser, JsonParsingException
from formatter import formatter


def validate(tokens) -> bool:
    parser = Parser()
    try:
        parser.parse(tokens)
    except JsonParsingException:
        return False
    return True


def main():
    lexer = Lexer()
    # tokens = lexer.lex('1')
    tokens = lexer.lex('{"foo": [1, 2, {"bar": 2}], "bar": true}')
    # print(tokens)
    # parser = Parser()
    # print(parser.parse(tokens))
    print(formatter(tokens))


if __name__ == "__main__":
    main()