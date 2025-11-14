# ================================================================
# ANALISADOR LÉXICO PARA A LINGUAGEM TONTO
# Revisado e Corrigido – Compatível com Windows + PLY + Parser
# ================================================================

import ply.lex as lex
import re

# ================================================================
# 1. PALAVRAS RESERVADAS E ESTEREÓTIPOS
# ================================================================
reserved = {
    # Palavras reservadas
    'package': 'RESERVED_WORD',
    'import': 'RESERVED_WORD',
    'genset': 'RESERVED_WORD',
    'disjoint': 'RESERVED_WORD',
    'complete': 'RESERVED_WORD',
    'general': 'RESERVED_WORD',
    'specifics': 'RESERVED_WORD',
    'where': 'RESERVED_WORD',
    'enum': 'RESERVED_WORD',

    # Tipos nativos
    'number': 'DATA_TYPE',
    'string': 'DATA_TYPE',
    'boolean': 'DATA_TYPE',
    'date': 'DATA_TYPE',
    'time': 'DATA_TYPE',
    'datetime': 'DATA_TYPE',

    # Estereótipos de classe
    'event': 'CLASS_STEREOTYPE',
    'situation': 'CLASS_STEREOTYPE',
    'process': 'CLASS_STEREOTYPE',
    'category': 'CLASS_STEREOTYPE',
    'mixin': 'CLASS_STEREOTYPE',
    'phaseMixin': 'CLASS_STEREOTYPE',
    'roleMixin': 'CLASS_STEREOTYPE',
    'kind': 'CLASS_STEREOTYPE',
    'collective': 'CLASS_STEREOTYPE',
    'quantity': 'CLASS_STEREOTYPE',
    'quality': 'CLASS_STEREOTYPE',
    'mode': 'CLASS_STEREOTYPE',
    'subkind': 'CLASS_STEREOTYPE',
    'phase': 'CLASS_STEREOTYPE',
    'role': 'CLASS_STEREOTYPE',

    # Estereótipos de relação
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
}

# ================================================================
# 2. LISTA DE TOKENS
# ================================================================
tokens = [
    'SPECIAL_SYMBOL',
    'CLASS_NAME',
    'RELATION_NAME',
    'INSTANCE_NAME',
    'NEW_TYPE',
    'NUMBER'
] + list(set(reserved.values()))

# ================================================================
# 3. EXPRESSÕES REGULARES DOS TOKENS
# ================================================================

# Símbolos especiais usados em relações
t_SPECIAL_SYMBOL = r'<>--|--<>|<o>--|--|\{|\}|\(|\)|\[|\]|:|,|@'

# Números simples
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Novos tipos, ex: AddressDataType
def t_NEW_TYPE(t):
    r'[A-Za-zÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑáàâãéèêíïóôõöúçñ]+DataType'
    return t

# Identificadores
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    # Palavra reservada ou estereótipo?
    t.type = reserved.get(t.value, 'IDENTIFIER')
    if t.type != 'IDENTIFIER':
        return t

    # Instância
    if re.fullmatch(r'[a-zA-Z_]+[0-9]+', t.value):
        t.type = 'INSTANCE_NAME'
        return t

    # Classe (começa com maiúscula)
    if re.match(r'^[A-Z]', t.value):
        t.type = 'CLASS_NAME'
        return t

    # Relação (começa com minúscula)
    t.type = 'RELATION_NAME'
    return t

# Comentários tipo "--- comentário"
def t_comment_tonto(t):
    r'\-\-\-.*'
    pass

# Comentários com #
def t_comment(t):
    r'\#.*'
    pass

# Ignorar espaços e tabs
t_ignore = " \t"

# Ignorar pontuações simples
t_ignore_PUNCTUATION = r"['\"!]"

# Registrar novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ERRO LÉXICO
def t_error(t):
    erros_lexicos.append(
        f"Erro Léxico: caractere inesperado '{t.value[0]}' na linha {t.lexer.lineno}."
    )
    t.lexer.skip(1)

# ================================================================
# 4. CONSTRUÇÃO DO LEXER (CORREÇÃO PARA WINDOWS!)
# ================================================================

def build_lexer():
    """Constrói lexer de forma compatível com Windows."""
    import lexico_tonto  # garante que PLY verá o módulo correto
    lexer = lex.lex(module=lexico_tonto, reflags=re.UNICODE)
    lexer.lineno = 1
    return lexer

# ================================================================
# 5. EXECUÇÃO DO LÉXICO EM UM ARQUIVO
# ================================================================

erros_lexicos = []

def analisar_arquivo(caminho):
    erros_lexicos.clear()
    tabela = []

    lexer = build_lexer()
    
    with open(caminho, 'r', encoding='utf-8') as arq:
        data = arq.read()

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break

        tabela.append({
            "tipo": tok.type,
            "valor": tok.value,
            "linha": tok.lineno,
            "posicao": tok.lexpos
        })

    return tabela, erros_lexicos
