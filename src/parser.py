import ply.yacc as yacc  # type: ignore
from src.lexer import tokens  # type: ignore # noqa


def p_start(p):
    '''start : elements'''
    # Remover último dicionário vazio, se existir
    if isinstance(p[1][-1], dict) and not p[1][-1]:
        p[1].pop()

    for article in p[1]:
        for field in ['title', 'author', 'abstract', 'year']:
            if field not in article:
                article[field] = ['']
    p[0] = p[1]


def p_elements(p):
    '''elements : elements element
                | element'''
    if len(p) == 3:
        p[0] = p[1]
        field, value = p[2]

        if not p[0] or not isinstance(p[0][-1], dict):
            p[0].append({})  # inicia novo artigo

        current = p[0][-1]
        if field not in current:
            current[field] = []

        if isinstance(value, list):
            for v in value:
                if v not in current[field]:
                    current[field].append(v)
        else:
            if value not in current[field]:
                current[field].append(value)
    else:
        field, value = p[1]
        article = {field: value if isinstance(value, list) else [value]}
        p[0] = [article]


def p_element(p):
    '''element : TITLE_OPEN TEXT TITLE_CLOSE
                | YEAR_OPEN TEXT YEAR_CLOSE'''
    tag = p.slice[1].type.lower().replace('_open', '')

    if len(p) == 4:
        p[0] = (tag, p[2])  # Ex: <Title>Texto</Title>
    else:
        # Ex: <Abstract><AbstractText>Texto</AbstractText></Abstract>
        p[0] = (tag, p[3])


def p_element_authorlist(p):
    '''element : AUTHORLIST_OPEN AUTHORS AUTHORLIST_CLOSE'''
    p[0] = ('author', p[2])  # ← também devolvemos tupla


def p_AUTHORS_multiple(p):  # Lista de autores
    '''AUTHORS : AUTHORS author'''
    p[0] = p[1] + [p[2]]


def p_AUTHORS_single(p):
    '''AUTHORS : author'''
    p[0] = [p[1]]


def p_author(p):
    '''
    author : AUTHOR_OPEN lastname forename AUTHOR_CLOSE
    '''
    p[0] = f"{p[3]} {p[2]}"


def p_lastname(p):
    '''
    lastname : LASTNAME_OPEN TEXT LASTNAME_CLOSE
    '''
    p[0] = p[2]


def p_forename(p):
    '''
    forename : FORENAME_OPEN TEXT FORENAME_CLOSE
    '''
    p[0] = p[2]


def p_element_abstract_multiple(p):
    '''element : ABSTRACT_OPEN abstract_texts ABSTRACT_CLOSE'''
    p[0] = ('abstract', p[2])  # Agora, passamos todos os textos para uma lista


def p_abstract_texts_multiple(p):
    '''abstract_texts : abstract_texts abstract_text'''
    p[0] = p[1] + [p[2]]  # Adiciona um novo abstract à lista


def p_abstract_texts_single(p):
    '''abstract_texts : abstract_text'''
    p[0] = [p[1]]  # Cria uma lista de um único abstract


def p_abstract_text(p):
    '''abstract_text : ABSTRACTTEXT_OPEN TEXT ABSTRACTTEXT_CLOSE'''
    p[0] = p[2]  # Captura o texto do abstract


def p_element_date_completed(p):
    '''element : DATECOMPLETED_OPEN YEAR_OPEN TEXT YEAR_CLOSE DATECOMPLETED_CLOSE'''
    p[0] = ('year', [p[3]])


def p_error(p):  # Tratamento de erro
    if p:
        print(f"Erro de sintaxe! Token inesperado: {p}")
    else:
        print("Erro de sintaxe! Fim inesperado do arquivo.")


# Criar o parser
parser = yacc.yacc()
