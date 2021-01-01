from sly import Parser
from treebuilder.FilterLexer import FilterLexer
from treebuilder.constants import ATTRIBUTES


class FilterParser(Parser):
    tokens = FilterLexer.tokens
    items = [{}]

    precedence = (
        ('left', AND, OR),
        ('left', EQ, NE),
        ('right', ATTR),
    )

    use_attributes = False

    # Grammar rules and actions
    @_('expr AND term')
    def expr(self, p):
        return [x and y for x, y in zip(p.expr, p.term)]

    @_('expr OR term')
    def expr(self, p):
        return [x or y for x, y in zip(p.expr, p.term)]
    
    @_('term')
    def expr(self, p):
        return p.term

    @_('term EQ factor')
    def term(self, p):
        return [p.term in x and x[p.term] == p.factor for x in self.__get_items()]

    @_('term NE factor')
    def term(self, p):
        return [p.term not in x or x[p.term] != p.factor for x in self.__get_items()]

    @_('ATTR factor')
    def term(self, p):
        self.use_attributes = True
        return p.factor

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('TEXT')
    def factor(self, p):
        return p.TEXT

    @_('ID')
    def factor(self, p):
        return p.ID

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    def __get_items(self):
        if self.use_attributes:
            self.use_attributes = False
            return (x[ATTRIBUTES] for x in self.items)
        return self.items
