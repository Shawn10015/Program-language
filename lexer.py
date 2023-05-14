import ply.lex as lex

tokens = (
   'NUMBER',
   'CURRENCY',
   'PLUS',
   'TIMES',
   'DECLARE',
   'ID',
)

t_PLUS    = r'\+'
t_TIMES   = r'\*'
t_NUMBER  = r'\d+'
t_DECLARE = r'declare'
t_ID = r'\w+'

# defined kind of currency
def t_CURRENCY(t):
    r'\d+\.\d\d(USD|EUR|JPY|RMB)'
    value, unit = float(t.value[:-3]), t.value[-3:]
    t.value = (value, unit)
    return t

t_ignore  = ' \t'

def t_error(t):
    print(f"Error word '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
