import ply.lex as lex
import re

# ==========================================================
# 1. Palavras reservadas e estereótipos (Sem alterações)
# ==========================================================
reserved = {
    'genset': 'RESERVED_WORD', 'disjoint': 'RESERVED_WORD', 'complete': 'RESERVED_WORD',
    'general': 'RESERVED_WORD', 'specifics': 'RESERVED_WORD', 'where': 'RESERVED_WORD', 'package': 'RESERVED_WORD',
    'event': 'CLASS_STEREOTYPE', 'situation': 'CLASS_STEREOTYPE', 'process': 'CLASS_STEREOTYPE',
    'category': 'CLASS_STEREOTYPE', 'mixin': 'CLASS_STEREOTYPE', 'phaseMixin': 'CLASS_STEREOTYPE',
    'roleMixin': 'CLASS_STEREOTYPE', 'historicalRoleMixin': 'CLASS_STEREOTYPE', 'kind': 'CLASS_STEREOTYPE',
    'collective': 'CLASS_STEREOTYPE', 'quantity': 'CLASS_STEREOTYPE', 'quality': 'CLASS_STEREOTYPE',
    'mode': 'CLASS_STEREOTYPE', 'intrisicMode': 'CLASS_STEREOTYPE', 'extrinsicMode': 'CLASS_STEREOTYPE',
    'subkind': 'CLASS_STEREOTYPE', 'phase': 'CLASS_STEREOTYPE', 'role': 'CLASS_STEREOTYPE', 'historicalRole': 'CLASS_STEREOTYPE',
    'material': 'RELATION_STEREOTYPE', 'derivation': 'RELATION_STEREOTYPE', 'comparative': 'RELATION_STEREOTYPE',
    'mediation': 'RELATION_STEREOTYPE', 'characterization': 'RELATION_STEREOTYPE', 'externalDependence': 'RELATION_STEREOTYPE',
    'componentOf': 'RELATION_STEREOTYPE', 'memberOf': 'RELATION_STEREOTYPE', 'subCollectionOf': 'RELATION_STEREOTYPE',
    'subQualityOf': 'RELATION_STEREOTYPE', 'instantiation': 'RELATION_STEREOTYPE', 'termination': 'RELATION_STEREOTYPE',
    'participational': 'RELATION_STEREOTYPE', 'participation': 'RELATION_STEREOTYPE', 'historicalDependence': 'RELATION_STEREOTYPE',
    'creation': 'RELATION_STEREOTYPE', 'manifestation': 'RELATION_STEREOTYPE', 'bringsAbout': 'RELATION_STEREOTYPE',
    'triggers': 'RELATION_STEREOTYPE', 'composition': 'RELATION_STEREOTYPE', 'aggregation': 'RELATION_STEREOTYPE',
    'inherence': 'RELATION_STEREOTYPE', 'value': 'RELATION_STEREOTYPE', 'formal': 'RELATION_STEREOTYPE', 'constitution': 'RELATION_STEREOTYPE',
    'ordered': 'META_ATTRIBUTE', 'const': 'META_ATTRIBUTE', 'derived': 'META_ATTRIBUTE',
    'subsets': 'META_ATTRIBUTE', 'redefines': 'META_ATTRIBUTE',
    'number': 'DATA_TYPE', 'string': 'DATA_TYPE', 'boolean': 'DATA_TYPE',
    'date': 'DATA_TYPE', 'time': 'DATA_TYPE', 'datetime': 'DATA_TYPE'
}

# ==========================================================
# 2. Lista de tokens (Sem alterações)
# ==========================================================
tokens = [
    'SPECIAL_SYMBOL', 'CLASS_NAME', 'RELATION_NAME', 'INSTANCE_NAME',
    'NEW_TYPE', 'NUMBER'
] + list(set(reserved.values()))

# ==========================================================
# 3. Regras Léxicas (Versão Final e Correta)
# ==========================================================

t_SPECIAL_SYMBOL = r'<>--|--<>|<o>--|--|\.\.|\{|\}|\(|\)|\[|\]|\*|@|:'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regra para novos tipos válidos. Precisa vir ANTES de t_IDENTIFIER para ter prioridade.
# A regra é estrita: apenas letras, terminando com 'DataType'.
def t_NEW_TYPE(t):
    r'[A-Za-zÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑáàâãéèêíïóôõöúçñ]+DataType'
    return t

# Regra única para todos os outros identificadores (válidos e inválidos)
def t_IDENTIFIER(t):
    r'[A-Za-zÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ_][A-Za-z0-9ÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ_]*'
    
    # 1. Checa se é uma palavra reservada
    t.type = reserved.get(t.value, 'IDENTIFIER')
    if t.type != 'IDENTIFIER':
        return t

    # 2. Checa por formatos inválidos que terminam com 'DataType'
    if t.value.endswith('DataType'):
        mensagem = (
            f"Erro Léxico: O nome de tipo '{t.value}' na linha {t.lexer.lineno} tem formato inválido. "
            f"Novos tipos não podem conter números ou sublinhados."
        )
        erros_lexicos.append(mensagem)
        return None # Descarta o token

    # 3. Separa a lógica principal
    has_number = re.search(r'\d', t.value)
    starts_with_upper = re.match(r'^[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]', t.value)

    if starts_with_upper:
        if has_number:
            mensagem = f"Erro Léxico: O nome de classe '{t.value}' na linha {t.lexer.lineno} não pode conter números."
            erros_lexicos.append(mensagem)
            return None
        else:
            t.type = 'CLASS_NAME'
            return t
    else: # Começa com letra minúscula
        if not has_number:
            t.type = 'RELATION_NAME'
            return t
        else: # Começa com minúscula e tem número
            if re.fullmatch(r'[a-záàâãéèêíïóôõöúçñ_][a-zA-Z0-9_]*[0-9]+', t.value):
                t.type = 'INSTANCE_NAME'
                return t
            else:
                mensagem = f"Erro Léxico: O identificador '{t.value}' na linha {t.lexer.lineno} contém números em posição inválida. Nomes de relação não podem ter números."
                erros_lexicos.append(mensagem)
                return None

def t_comment_tonto(t):
    r'\-\-\-.*'
    pass

def t_comment(t):
    r'\#.*'
    pass

t_ignore = ' \t'
t_ignore_PUNCTUATION = r"[.,'\"!?]"

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
# 4. Função para construir o lexer (Sem alterações)
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
