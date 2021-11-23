from constants import *

FOUR_SPACES = "    "

def format_json(tokens, indentation_type=FOUR_SPACES):
    indentation = 0
    formatted_json = ''

    for i, token in enumerate(tokens):
        if token in (OPENBRACE, OPENBRACKET):
            if tokens[i-1] == COLON:
                formatted_json += f'{token}\n'
            else:
                formatted_json += f'{indentation*indentation_type}{token}\n'
            indentation += 1
            continue
        
        if token in (CLOSEBRACE, CLOSEBRACKET):
            indentation -= 1
            formatted_json += f'\n{indentation*indentation_type}{token}'  
            continue

        if token == COMMA:
            formatted_json += f'{token}\n'
            continue

        if token == COLON:
            formatted_json += f'{token} '
            continue

        if tokens[i-1] == COLON:
            if type(token) is str:
                formatted_json += f'"{token}"'
            elif token is None:
                formatted_json += 'null'
            else:
                formatted_json += str(token).lower()
            continue

        if type(token) is str:
            formatted_json += f'{indentation*indentation_type}"{token}"'
            continue
        
        if token is None:
            formatted_json += f'{indentation*indentation_type}null'
            continue

        formatted_json += f'{indentation*indentation_type}{str(token).lower()}'
    
    return formatted_json
    