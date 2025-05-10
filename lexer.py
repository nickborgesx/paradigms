import ply.lex as lex

# Lista de tokens que vamos usar
tokens = (
    'TITLE_OPEN', 'TITLE_CLOSE',
    'AUTHOR_OPEN', 'AUTHOR_CLOSE',
    'ABSTRACT_OPEN', 'ABSTRACT_CLOSE',
    'YEAR_OPEN', 'YEAR_CLOSE',
    'TEXT'
)

# Expressões regulares para identificar as tags
t_TITLE_OPEN = r'<title>'
t_TITLE_CLOSE = r'</title>'
t_AUTHOR_OPEN = r'<author>'
t_AUTHOR_CLOSE = r'</author>'
t_ABSTRACT_OPEN = r'<abstract>'
t_ABSTRACT_CLOSE = r'</abstract>'
t_YEAR_OPEN = r'<year>'
t_YEAR_CLOSE = r'</year>'

# Ignorar espaços e quebras de linha
t_ignore = ' \t\n'

# Texto entre as tags (qualquer coisa que não seja uma tag)
def t_TEXT(t):
    r'[^<>]+'
    t.value = t.value.strip()
    return t

# Tratamento de erro léxico
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()
