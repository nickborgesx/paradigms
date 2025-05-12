import ply.yacc as yacc  # type: ignore
from lexer import tokens  # type: ignore # noqa

# Lista para armazenar os artigos extraídos
articles = []

# Objeto temporário para armazenar um artigo
current_article = {}


def p_start(p):  # Regra inicial: um ou mais elementos
    '''start : elements'''
    p[0] = p[1]

# Lista de elementos


def p_elements(p):
    '''elements : elements element
                | element'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]


def p_element(p):  # Elementos que armazenamos diretamente
    '''element : TITLE_OPEN TEXT TITLE_CLOSE
               | ABSTRACT_OPEN TEXT ABSTRACT_CLOSE
               | YEAR_OPEN TEXT YEAR_CLOSE'''
    tag = p.slice[1].type.lower().replace(
        '_open', '')  # exemplo: TITLE_OPEN -> title
    global current_article
    if tag not in current_article:
        current_article[tag] = []
    current_article[tag].append(p[2])

    # Quando ano for encontrado, salva o artigo
    if tag == 'year':
        articles.append(current_article)
        current_article = {}


def p_element_authorlist(p):  # Elemento de lista de autores
    '''element : AUTHORLIST_OPEN AUTHORS AUTHORLIST_CLOSE'''
    global current_article
    if 'author' not in current_article:
        current_article['author'] = []
    # p[2] é a lista de autores extraída
    current_article['author'].extend(p[2])


def p_AUTHORS_multiple(p):  # Lista de autores
    '''AUTHORS : AUTHORS author'''
    p[0] = p[1] + [p[2]]


def p_AUTHORS_single(p):
    '''AUTHORS : author'''
    p[0] = [p[1]]


def p_author(p):  # Um único autor
    '''author : AUTHOR_OPEN author_data AUTHOR_CLOSE'''
    p[0] = p[2]


def p_author_data(p):  # Dados do autor: forename + lastname
    '''author_data : FORENAME_OPEN TEXT FORENAME_CLOSE LASTNAME_OPEN TEXT LASTNAME_CLOSE'''
    fore = p[2]
    last = p[5]
    p[0] = f'{fore} {last}'


def p_error(p):  # Tratamento de erro
    if p:
        print(f"Erro de sintaxe! Token inesperado: {p}")
    else:
        print("Erro de sintaxe! Fim inesperado do arquivo.")


# Criar o parser
parser = yacc.yacc()
