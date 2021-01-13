from treebuilder.FilterLexer import FilterLexer
from treebuilder.FilterParser import FilterParser
from treebuilder.constants import ATTRIBUTES


class TestFilterParser:
    
    lexer = FilterLexer()
    items = [
        { 'Name': 'foo', 'Value': '10', 'title': 'foo' },
        { 'Name': 'bar', 'Value': '20', 'title': 'bar' },
        { 'Value': '20', 'title': 'bar' }
    ]

    def test_equal(self):
        parser = FilterParser()
        parser.items = self.items

        syntax = 'Name=foo'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [True, False, False] == result

    def test_not_equal(self):
        parser = FilterParser()
        parser.items = self.items

        syntax = 'Name != foo'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, True] == result

    def test_and_operator(self):
        parser = FilterParser()
        parser.items = self.items

        syntax = 'Name=foo and title=foo'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [True, False, False] == result

        syntax = 'Name=foo and title=bar'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, False, False] == result

    def test_or_operator(self):
        parser = FilterParser()
        parser.items = self.items

        syntax = 'Name=foo or title=foo'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [True, False, False] == result

        syntax = 'Name=foo or title=bar'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [True, True, True] == result

    def test_or_and_and_operator(self):
        parser = FilterParser()
        parser.items = self.items

        syntax = 'Name=foo or Name=bar and Value=20'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, False] == result

    def test_and_and_or_operator(self):
        parser = FilterParser()
        parser.items = self.items

        syntax = 'Name=foo and Name=bar or Value=20'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, True] == result

    def test_parenthesis(self):
        parser = FilterParser()
        parser.items = self.items

        syntax = '(Name=foo and Name=bar) or Value=20'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, True] == result

        syntax = 'Name=foo and (Name=bar or Value=20)'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, False, False] == result

        syntax = 'Name=bar and (title=foo or Value=20)'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, False] == result

    def test_attributes(self):
        parser = FilterParser()
        parser.items = [
            { 'Name': 'foo', ATTRIBUTES: { 'xsi:type': 'FooType', 'title': 'foo' } },
            { 'Name': 'bar',  ATTRIBUTES: { 'xsi:type': 'BarType', 'title': 'bar' } },
            { 'Name': 'other', ATTRIBUTES: { 'xsi:type': 'BarType', 'title': 'other' } }
        ]

        syntax = '@title=foo'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [True, False, False] == result

        syntax = '@title != foo'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, True] == result

        syntax = '@xsi:type = BarType'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, True] == result

        syntax = '@xsi:type = BarType and Name=bar'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, True, False] == result

        syntax = 'Name != bar or @xsi:type = BarType'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [True, True, True] == result

        syntax = '@title=other and @xsi:type = BarType'
        result = parser.parse(self.lexer.tokenize(syntax))
        assert [False, False, True] == result
