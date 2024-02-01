import ply.lex as lex

reserved = ( 'CHAR', 'INT', 'WHILE', 'ELSE', 'EXIT', 'FLOAT', 'IF', 'READ', 'WRITE', 'RETURN', 'VOID')

tokens = reserved + ('NOT', 'OR', 'AND', 'LE', 'LT', 'GE', 'GT', 'EQ', 'NE', 'ASSIGN', 'SEMICOLON',
          'LBRACE','RBRACE', 'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'PLUS', 'MINUS',
          'TIMES','DIVIDE','COMMA','STRING','IDENTIFIER','INTCON', 'FLOATCON', 'CHARCON')


reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

def t_IDENTIFIER(t):
    r'[a-zA-Z]([a-zA-Z]|[0-9])*'
    t.type = reserved_map.get(t.value,'IDENTIFIER');
    return t

t_NOT = r'!'
t_OR = r'\|\|'
t_AND= r'&&'
t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_EQ = r'=='
t_NE = r'!='
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','
t_STRING = r'\"[^\"]*\"'
t_CHARCON = r'\'[^\']\''

	
def t_FLOATCON(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t
	
def t_INTCON(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\/\/.* | \/\*([^\/])*\*\/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_WS(t):
    r'[ \t]'
    pass

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_eof(t):
    return None

lexer = lex.lex()
if __name__ == "__main__":
    lex.runmain(lexer)