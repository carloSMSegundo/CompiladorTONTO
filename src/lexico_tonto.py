import ply.lex as lex
import re

# ==========================================================
# 1. Palavras reservadas e estereótipos
# ==========================================================
reserved = {
    # Palavras reservadas
    'genset': 'RESERVED_WORD', 'disjoint': 'RESERVED_WORD', 'complete': 'RESERVED_WORD',
    'general': 'RESERVED_WORD', 'specifics': 'RESERVED_WORD', 'where': 'RESERVED_WORD', 
    'package': 'RESERVED_WORD', 'import': 'RESERVED_WORD', 'functional-complexes': 'RESERVED_WORD',
    'intrinsic-modes': 'RESERVED_WORD', 'relators': 'RESERVED_WORD',

    # Estereótipos de classe
    'event': 'CLASS_STEREOTYPE', 'situation': 'CLASS_STEREOTYPE', 'process': 'CLASS_STEREOTYPE',
    'category': 'CLASS_STEREOTYPE', 'mixin': 'CLASS_STEREOTYPE', 'phaseMixin': 'CLASS_STEREOTYPE',
    'roleMixin': 'CLASS_STEREOTYPE', 'historicalRoleMixin': 'CLASS_STEREOTYPE', 'kind': 'CLASS_STEREOTYPE',
    'collective': 'CLASS_STEREOTYPE', 'quantity': 'CLASS_STEREOTYPE', 'quality': 'CLASS_STEREOTYPE',
    'mode': 'CLASS_STEREOTYPE', 'intrisicMode': 'CLASS_STEREOTYPE', 'extrinsicMode': 'CLASS_STEREOTYPE',
    'subkind': 'CLASS_STEREOTYPE', 'phase': 'CLASS_STEREOTYPE', 'role': 'CLASS_STEREOTYPE', 'historicalRole': 'CLASS_STEREOTYPE',

    # Estereótipos de relação
    'material': 'RELATION_STEREOTYPE', 'derivation': 'RELATION_STEREOTYPE', 'comparative': 'RELATION_STEREOTYPE',
    'mediation': 'RELATION_STEREOTYPE', 'characterization': 'RELATION_STEREOTYPE',
    'externalDependence': 'RELATION_STEREOTYPE', 'componentOf': 'RELATION_STEREOTYPE', 'memberOf': 'RELATION_STEREOTYPE',
    'subCollectionOf': 'RELATION_STEREOTYPE', 'subQualityOf': 'RELATION_STEREOTYPE', 'instantiation': 'RELATION_STEREOTYPE',
    'termination': 'RELATION_STEREOTYPE', 'participational': 'RELATION_STEREOTYPE', 'participation': 'RELATION_STEREOTYPE',
    'historicalDependence': 'RELATION_STEREOTYPE', 'creation': 'RELATION_STEREOTYPE', 'manifestation': 'RELATION_STEREOTYPE',
    'bringsAbout': 'RELATION_STEREOTYPE', 'triggers': 'RELATION_STEREOTYPE', 'composition': 'RELATION_STEREOTYPE',
    'aggregation': 'RELATION_STEREOTYPE', 'inherence': 'RELATION_STEREOTYPE', 'value': 'RELATION_STEREOTYPE',
    'formal': 'RELATION_STEREOTYPE', 'constitution': 'RELATION_STEREOTYPE',

    # Meta-atributos
    'ordered': 'META_ATTRIBUTE', 'const': 'META_ATTRIBUTE', 'derived': 'META_ATTRIBUTE',
    'subsets': 'META_ATTRIBUTE', 'redefines': 'META_ATTRIBUTE',

    # Tipos de dados nativos
    'number': 'DATA_TYPE', 'string': 'DATA_TYPE', 'boolean': 'DATA_TYPE',
    'date': 'DATA_TYPE', 'time': 'DATA_TYPE', 'datetime': 'DATA_TYPE'
}

# ==========================================================
# 2. Lista de tokens
# ==========================================================
tokens = [
    'SPECIAL_SYMBOL', 'CLASS_NAME', 'RELATION_NAME', 'INSTANCE_NAME',
    'NEW_TYPE', 'NUMBER'
] + list(set(reserved.values()))

# ==========================================================
# 3. Regras Léxicas
# ==========================================================

# Símbolos especiais
t_SPECIAL_SYMBOL = r'<>--|--<>|<o>--|--|\.\.|\{|\}|\(|\)|\[|\]|\*|@|\.'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEW_TYPE(t):
    r'[A-Za-zÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑáàâãéèêíïóôõöúçñ]+DataType'
    if '_' in t.value or any(char.isdigit() for char in t.value):
        mensagem = (
            f"Erro Léxico: O nome de tipo '{t.value}' na linha {t.lexer.lineno} tem formato inválido. "
            f"Novos tipos não podem conter números ou sublinhados."
        )
        erros_lexicos.append(mensagem)
        return None
    return t

# Regra para identificadores - incluindo hífen APENAS para as palavras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_-]*'
    
    t.type = reserved.get(t.value, 'IDENTIFIER')
    
    # Se for uma palavra reservada (incluindo as com hífen), retorna
    if t.type != 'IDENTIFIER':
        return t

    # Se não for palavra reservada, verifica se tem hífen (o que é um erro)
    if '-' in t.value:
        mensagem = f"Erro Léxico: O identificador '{t.value}' na linha {t.lexer.lineno} não pode conter hífens, pois não é uma palavra reservada."
        erros_lexicos.append(mensagem)
        return None

    # Lógica para nomes com e sem números
    has_number = re.search(r'\d', t.value)
    if not has_number:
        if re.match(r'^[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]', t.value):
            t.type = 'CLASS_NAME'
        else:
            t.type = 'RELATION_NAME'
        return t
    else:
        if re.fullmatch(r'[A-Za-zÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ_]+[0-9]+', t.value):
            t.type = 'INSTANCE_NAME'
            return t
        else:
            if re.match(r'^[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]', t.value):
                mensagem = f"Erro Léxico: O nome de classe '{t.value}' na linha {t.lexer.lineno} não pode conter números."
            else:
                mensagem = f"Erro Léxico: O nome de relação '{t.value}' na linha {t.lexer.lineno} não pode conter números."
            erros_lexicos.append(mensagem)
            return None

def t_comment_tonto(t):
    r'\-\-\-.*'
    pass

def t_comment(t):
    r'\#.*'
    pass

t_ignore = ' \t'
t_ignore_PUNCTUATION = r"[,':\"!?]"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    char = t.value[0]
    mensagem = (
        f"Erro Léxico: Caractere inesperado '{char}' na linha {t.lexer.lineno}. "
        f"Sugestão: Verifique se o símbolo é permitido na linguagem TONTO ou se há um erro de digitação."
    )
    erros_lexicos.append(mensagem)
    t.lexer.skip(1)

# ==========================================================
# 4. Função para construir o lexer e executar a análise
# ==========================================================
erros_lexicos = []

def analisar_arquivo(caminho_arquivo):
    erros_lexicos.clear()
    lexer = lex.lex()
    tabela_de_simbolos = []
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        data = f.read()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: break
        tabela_de_simbolos.append({
            'tipo': tok.type,
            'valor': tok.value,
            'linha': tok.lineno,
            'posicao': tok.lexpos
        })
    return tabela_de_simbolos, erros_lexicos