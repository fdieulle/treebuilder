from sly import Lexer


class FilterLexer(Lexer):
    
    tokens = {
        ID, TEXT, NUMBER,
        AND, OR,
        EQ, NE,
        LPAREN, RPAREN,
        ATTR
    }

    ignore = ' \t'
    
    ID =     r'[a-zA-Z_\:][a-zA-Z0-9_\:]*'
    TEXT =   r'(?P<quote>["\']).*?(?P=quote)'
    NUMBER = r'\d+(\.\d+)?'

    ID['and'] = AND
    ID['or']  = OR

    EQ = r'='
    NE = r'!='

    LPAREN  = r'\('
    RPAREN  = r'\)'

    ATTR = r'@'

    def TEXT(self, t):
        t.value = t.value[1:-1]
        return t
