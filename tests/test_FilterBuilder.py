import unittest
from treebuilder.FilterLexer import FilterLexer


class TestFilterLexer(unittest.TestCase):
    def test_equals(self):
        lexer = FilterLexer()

        syntax = 'Name=Value'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'ID'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'Value'], [tok['value'] for tok in tokens])

    def test_not_equals(self):
        lexer = FilterLexer()

        syntax = 'Name != Value'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'NE', 'ID'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '!=', 'Value'], [tok['value'] for tok in tokens])

    def test_quoted_value(self):
        lexer = FilterLexer()

        syntax = 'Name=\'Value\''
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'TEXT'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'Value'], [tok['value'] for tok in tokens])

    def test_double_quoted_value(self):
        lexer = FilterLexer()

        syntax = 'Name="Value"'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'TEXT'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'Value'], [tok['value'] for tok in tokens])

    def test_text_with_space_and_quoted_value(self):
        lexer = FilterLexer()

        syntax = "Name = 'Value is protected'"
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'TEXT'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'Value is protected'], [tok['value'] for tok in tokens])

    def test_text_with_space_and_double_quoted_value(self):
        lexer = FilterLexer()

        syntax = 'Name = "Value is protected"'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'TEXT'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'Value is protected'], [tok['value'] for tok in tokens])

    def test_with_number(self):
        lexer = FilterLexer()

        syntax = 'Property1=10'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'NUMBER'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Property1', '=', '10'], [tok['value'] for tok in tokens])

    def test_with_floating_number(self):
        lexer = FilterLexer()
        syntax = 'Property1=10.5'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'NUMBER'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Property1', '=', '10.5'], [tok['value'] for tok in tokens])

    def test_and_operator(self):
        lexer = FilterLexer()
        syntax = 'Name=Value and Property1!=10'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'ID', 'AND', 'ID', 'NE', 'NUMBER'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'Value', 'and', 'Property1', '!=', '10'], [tok['value'] for tok in tokens])

    def test_or_operator(self):
        lexer = FilterLexer()
        syntax = 'Name="Value is protected" or Property1!=10'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'TEXT', 'OR', 'ID', 'NE', 'NUMBER'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'Value is protected', 'or', 'Property1', '!=', '10'], [tok['value'] for tok in tokens])

    def test_and_and_or_operator(self):
        lexer = FilterLexer()
        syntax = 'Name = foo or Property1 != 10 and Property2 = bar'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ID', 'EQ', 'ID', 'OR', 'ID', 'NE', 'NUMBER', 'AND', 'ID', 'EQ', 'ID'], [tok['type'] for tok in tokens])
        self.assertListEqual(['Name', '=', 'foo', 'or', 'Property1', '!=', '10', 'and', 'Property2', '=', 'bar'], [tok['value'] for tok in tokens])

    def test_attribute(self):
        lexer = FilterLexer()

        syntax = '@Name=Value'
        tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
        
        self.assertListEqual(['ATTR', 'ID', 'EQ', 'ID'], [tok['type'] for tok in tokens])
        self.assertListEqual(['@', 'Name', '=', 'Value'], [tok['value'] for tok in tokens])



if __name__ == '__main__':
    unittest.main()