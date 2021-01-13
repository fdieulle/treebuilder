from treebuilder.FilterLexer import FilterLexer


def test_equals():
    lexer = FilterLexer()

    syntax = 'Name=Value'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'ID'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'Value'] == [tok['value'] for tok in tokens]


def test_not_equals():
    lexer = FilterLexer()

    syntax = 'Name != Value'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'NE', 'ID'] == [tok['type'] for tok in tokens]
    assert ['Name', '!=', 'Value'] == [tok['value'] for tok in tokens]


def test_quoted_value():
    lexer = FilterLexer()

    syntax = 'Name=\'Value\''
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'TEXT'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'Value'] == [tok['value'] for tok in tokens]


def test_double_quoted_value():
    lexer = FilterLexer()

    syntax = 'Name="Value"'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'TEXT'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'Value'] == [tok['value'] for tok in tokens]


def test_text_with_space_and_quoted_value():
    lexer = FilterLexer()

    syntax = "Name = 'Value is protected'"
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'TEXT'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'Value is protected'] == [tok['value'] for tok in tokens]


def test_text_with_space_and_double_quoted_value():
    lexer = FilterLexer()

    syntax = 'Name = "Value is protected"'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'TEXT'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'Value is protected'] == [tok['value'] for tok in tokens]


def test_with_number():
    lexer = FilterLexer()

    syntax = 'Property1=10'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'NUMBER'] == [tok['type'] for tok in tokens]
    assert ['Property1', '=', '10'] == [tok['value'] for tok in tokens]


def test_with_floating_number():
    lexer = FilterLexer()
    syntax = 'Property1=10.5'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'NUMBER'] == [tok['type'] for tok in tokens]
    assert ['Property1', '=', '10.5'] == [tok['value'] for tok in tokens]


def test_and_operator():
    lexer = FilterLexer()
    syntax = 'Name=Value and Property1!=10'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'ID', 'AND', 'ID', 'NE', 'NUMBER'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'Value', 'and', 'Property1', '!=', '10'] == [tok['value'] for tok in tokens]


def test_or_operator():
    lexer = FilterLexer()
    syntax = 'Name="Value is protected" or Property1!=10'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'TEXT', 'OR', 'ID', 'NE', 'NUMBER'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'Value is protected', 'or', 'Property1', '!=', '10'] == [tok['value'] for tok in tokens]


def test_and_and_or_operator():
    lexer = FilterLexer()
    syntax = 'Name = foo or Property1 != 10 and Property2 = bar'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ID', 'EQ', 'ID', 'OR', 'ID', 'NE', 'NUMBER', 'AND', 'ID', 'EQ', 'ID'] == [tok['type'] for tok in tokens]
    assert ['Name', '=', 'foo', 'or', 'Property1', '!=', '10', 'and', 'Property2', '=', 'bar'] == [tok['value'] for tok in tokens]


def test_attribute():
    lexer = FilterLexer()

    syntax = '@Name=Value'
    tokens = [{'type': tok.type, 'value': tok.value} for tok in lexer.tokenize(syntax)]
    
    assert ['ATTR', 'ID', 'EQ', 'ID'] == [tok['type'] for tok in tokens]
    assert ['@', 'Name', '=', 'Value'] == [tok['value'] for tok in tokens]