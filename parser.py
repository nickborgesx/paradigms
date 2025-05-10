import ply.yacc as yacc
from lexer import tokens

# Lista para armazenar os artigos extraídos
articles = []

# Objeto temporário para armazenar um artigo
current_article = {}

# Regra inicial: um ou mais elementos
def p_start(p):
    '''start : elements'''
    p[0] = p[1]

# Lista de elementos (tags como title, author etc)
def p_elements(p):
    '''elements : elements element
                | element'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]

# Cada elemento pode ser título, autor, etc.
def p_element(p):
    '''element : TITLE_OPEN TEXT TITLE_CLOSE
               | AUTHOR_OPEN TEXT AUTHOR_CLOSE
               | ABSTRACT_OPEN TEXT ABSTRACT_CLOSE
               | YEAR_OPEN TEXT YEAR_CLOSE'''
    tag = p.slice[1].type.lower().replace('_open', '')  # exemplo: TITLE_OPEN -> 'title'
    global current_article
    if tag not in current_article:
        current_article[tag] = []
    current_article[tag].append(p[2])

    # Quando ano for encontrado, salvamos o artigo
    if tag == 'year':
        articles.append(current_article)
        current_article = {}

# Erro de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe! Token inesperado: {p}")
    else:
        print("Erro de sintaxe! Fim inesperado do arquivo.")

# Criar o parser
parser = yacc.yacc()
