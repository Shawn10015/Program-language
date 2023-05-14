import ply.yacc as yacc
from lexer import tokens, lexer

symbol_table = {}
#information about convert
exchange_rates = {'USD': 1.0, 'EUR': 0.9, 'JPY': 110.0, 'RMB': 6.9} 

#define some rules about expression like: declare a 30, declare a 30.00USD
def p_expression_declare(p):
    'expression : DECLARE ID factor'
    symbol_table[p[2]] = p[3]
    p[0] = p[3]

def p_expression_plus(p):
    'expression : expression PLUS term'
    if p[1]['type'] == p[3]['type']:
        if p[1]['type'] == 'number':
            p[0] = {'type': 'number', 'value': p[1]['value'] + p[3]['value'], 'unit': p[1]['unit']}
        elif p[1]['type'] == 'currency':
            if p[1]['unit'] == p[3]['unit']:
                p[0] = {'type': 'currency', 'value': p[1]['value'] + p[3]['value'], 'unit': p[1]['unit']}
            else:
                converted_value = p[3]['value'] * exchange_rates[p[3]['unit']] / exchange_rates[p[1]['unit']]
                p[0] = {'type': 'currency', 'value': p[1]['value'] + converted_value, 'unit': p[1]['unit']}
                p[0]['original_unit'] = p[3]['unit']
                p[0]['target_unit'] = p[1]['unit']
        else:
            print('Error')
    else:
        print('Type error')

#define some rules like, a,3
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = {'type': 'number', 'value': int(p[1]), 'unit': 'USD'}

def p_factor_currency(p):
    'factor : CURRENCY'
    value, unit = p[1]
    value = float(value)
    #convert to USD
    if unit == 'EUR':
        value /= exchange_rates['EUR'] 
        p[0] = {'type': 'currency', 'value': value, 'unit': 'USD', 'original_unit': 'EUR'}
    elif unit == 'JPY':
        value /= exchange_rates['JPY']
        p[0] = {'type': 'currency', 'value': value, 'unit': 'USD', 'original_unit': 'JPY'}
    elif unit == 'RMB':
        value /= exchange_rates['RMB']
        p[0] = {'type': 'currency', 'value': value, 'unit': 'USD', 'original_unit': 'RMB'}
    else:
        p[0] = {'type': 'currency', 'value': value, 'unit': unit}


def p_factor_id(p):
    'factor : ID'
    if p[1] in symbol_table:
        p[0] = symbol_table[p[1]]
    else:
        print(f'Error: variable {p[1]} is not declared')
        p[0] = {'type': 'number', 'value': 0, 'unit': 'USD'}

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print('Error')

parser = yacc.yacc()
