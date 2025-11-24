# src/lexico_tonto.py
import ply.lex as lex
import re

# ================================================================
# 1. PALAVRAS RESERVADAS
# ================================================================
reserved = {
    'package': 'KW_PACKAGE',
    'import': 'KW_IMPORT',
    'genset': 'KW_GENSET',
    'disjoint': 'KW_DISJOINT',
    'complete': 'KW_COMPLETE',
    'general': 'KW_GENERAL',
    'specifics': 'KW_SPECIFICS',
    'where': 'KW_WHERE',
    'enum': 'KW_ENUM',
    'specializes': 'KW_SPECIALIZES',
    'relation': 'KW_RELATION',
    'of': 'KW_OF',
    'datatype': 'KW_DATATYPE', # <-- ADICIONAR

    # Tipos
    'number': 'DATA_TYPE',
    'string': 'DATA_TYPE',
    'boolean': 'DATA_TYPE',
    'date': 'DATA_TYPE',
    'time': 'DATA_TYPE',
    'datetime': 'DATA_TYPE',
    'int': 'DATA_TYPE',

    # Estereótipos de Classe
    'kind': 'CLASS_STEREOTYPE',
    'subkind': 'CLASS_STEREOTYPE',
    'role': 'CLASS_STEREOTYPE',
    'phase': 'CLASS_STEREOTYPE',
    'category': 'CLASS_STEREOTYPE',
    'mixin': 'CLASS_STEREOTYPE',
    'roleMixin': 'CLASS_STEREOTYPE',
    'phaseMixin': 'CLASS_STEREOTYPE',
    'relator': 'CLASS_STEREOTYPE',
    'mode': 'CLASS_STEREOTYPE',
    'quality': 'CLASS_STEREOTYPE',
    'quantity': 'CLASS_STEREOTYPE',
    'collective': 'CLASS_STEREOTYPE',
    'event': 'CLASS_STEREOTYPE',
    'situation': 'CLASS_STEREOTYPE',
    'process': 'CLASS_STEREOTYPE',
    'historicalRole': 'CLASS_STEREOTYPE',
    'historicalRoleMixin': 'CLASS_STEREOTYPE',
    'type': 'CLASS_STEREOTYPE',

    # Estereótipos de Relação
    'material': 'RELATION_STEREOTYPE',
    'derivation': 'RELATION_STEREOTYPE',
    'comparative': 'RELATION_STEREOTYPE',
    'mediation': 'RELATION_STEREOTYPE',
    'characterization': 'RELATION_STEREOTYPE',
    'componentOf': 'RELATION_STEREOTYPE',
    'memberOf': 'RELATION_STEREOTYPE',
    'subCollectionOf': 'RELATION_STEREOTYPE',
    'subQualityOf': 'RELATION_STEREOTYPE',
    'instantiation': 'RELATION_STEREOTYPE',
    'creation': 'RELATION_STEREOTYPE',
    'composition': 'RELATION_STEREOTYPE',
    'participation': 'RELATION_STEREOTYPE',
}

# ================================================================
# 2. LISTA DE TOKENS
# ================================================================
tokens = [
             'CLASS_NAME', 'RELATION_NAME', 'INSTANCE_NAME', 'NEW_TYPE', 'NUMBER',
             'REL_SYM', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
             'LPAREN', 'RPAREN', 'COLON', 'COMMA', 'AT', 'RANGE_DOTS', 'STAR',
             'SPECIAL_SYMBOL'
         ] + list(set(reserved.values()))

# ================================================================
# 3. REGRAS DE TOKENS
# ================================================================
t_REL_SYM = r'<>--|--<>|<o>--|--'
t_RANGE_DOTS = r'\.\.'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','
t_AT = r'@'
t_STAR = r'\*'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NEW_TYPE(t):
    r'[A-Za-zÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑáàâãéèêíïóôõöúçñ]+DataType'
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_\-]*'  # Aceita hífens para "functional-complexes"

    if t.value in reserved:
        t.type = reserved[t.value]
        return t

    if t.value[0].isupper():
        t.type = 'CLASS_NAME'
        return t

    if re.search(r'\d+$', t.value):
        t.type = 'INSTANCE_NAME'
        return t

    t.type = 'RELATION_NAME'
    return t

t_ignore = " \t\n"


def t_comment(t):
    r'(\-\-\-.*)|(\#.*)|(//.*)'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


erros_lexicos = []


def t_error(t):
    erros_lexicos.append(f"Erro Léxico: caractere inesperado '{t.value[0]}' na linha {t.lexer.lineno}.")
    t.lexer.skip(1)


def build_lexer():
    import lexico_tonto
    return lex.lex(module=lexico_tonto, reflags=re.UNICODE)


def analisar_arquivo(caminho):
    erros_lexicos.clear()
    tabela = []
    lexer = build_lexer()
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            data = f.read()
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: break
            tabela.append({"tipo": tok.type, "valor": tok.value, "linha": tok.lineno, "posicao": tok.lexpos})
    except Exception as e:
        print(f"Erro: {e}")
    return tabela, erros_lexicos