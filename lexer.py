import ply.lex as lex  # type: ignore

# Lista de tokens reconhecidos pelo lexer
tokens = (
    'TITLE_OPEN', 'TITLE_CLOSE',
    'AUTHORLIST_OPEN', 'AUTHORLIST_CLOSE',
    'AUTHOR_OPEN', 'AUTHOR_CLOSE',
    'LASTNAME_OPEN', 'LASTNAME_CLOSE',
    'FORENAME_OPEN', 'FORENAME_CLOSE',
    'ABSTRACT_OPEN', 'ABSTRACT_CLOSE',
    'YEAR_OPEN', 'YEAR_CLOSE',
    'TEXT',
)

# Expressões regulares para identificar cada tag de abertura e fechamento
t_TITLE_OPEN = r'<Title>'
t_TITLE_CLOSE = r'</Title>'
t_LASTNAME_OPEN = r'<LastName>'
t_LASTNAME_CLOSE = r'</LastName>'
t_FORENAME_OPEN = r'<ForeName>'
t_FORENAME_CLOSE = r'</ForeName>'
t_ABSTRACT_OPEN = r'<Abstract>'
t_ABSTRACT_CLOSE = r'</Abstract>'
t_YEAR_OPEN = r'<Year>'
t_YEAR_CLOSE = r'</Year>'


def t_AUTHORLIST_OPEN(t):
    r'<AuthorList(\s+[^>]*)?>'
    return t


def t_AUTHORLIST_CLOSE(t):
    r'</AuthorList>'
    return t


def t_AUTHOR_OPEN(t):
    r'<Author(\s+[^>]*)?>'
    return t


def t_AUTHOR_CLOSE(t):
    r'</Author>'
    return t


# Ignorar espaços e quebras de linha
t_ignore = ' \t\n'


def t_TEXT(t):  # Texto entre tags (qualquer coisa que não seja '<' ou '>')
    r'[^<>]+'
    t.value = t.value.strip()
    return t


def t_error(t):  # Tratamento de erro léxico
    # Ignora tags XML desconhecidas
    if t.value.startswith("<"):
        end = t.value.find(">")
        if end != -1:
            t.lexer.skip(end + 1)
            return
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


# Criar o lexer
lexer = lex.lex()
