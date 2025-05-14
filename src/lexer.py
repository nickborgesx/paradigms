import ply.lex as lex  # type: ignore

# Lista de tokens reconhecidos pelo lexer
tokens = (
    'TITLE_OPEN', 'TITLE_CLOSE',
    'AUTHORLIST_OPEN', 'AUTHORLIST_CLOSE',
    'AUTHOR_OPEN', 'AUTHOR_CLOSE',
    'LASTNAME_OPEN', 'LASTNAME_CLOSE',
    'FORENAME_OPEN', 'FORENAME_CLOSE',
    'ABSTRACTTEXT_OPEN', 'ABSTRACTTEXT_CLOSE',
    'ABSTRACT_OPEN', 'ABSTRACT_CLOSE',
    'DATECOMPLETED_OPEN', 'DATECOMPLETED_CLOSE',
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
t_ABSTRACTTEXT_CLOSE = r'</AbstractText>'
t_DATECOMPLETED_OPEN = r'<DateCompleted>'
t_DATECOMPLETED_CLOSE = r'</DateCompleted>'
t_YEAR_OPEN = r'<Year>'
t_YEAR_CLOSE = r'</Year>'


def t_LANGUAGE(t):
    r'<Language>.*?</Language>'
    return None


def t_ISSN(t):
    r'<ISSN.*?>.*?</ISSN>'
    return None


def t_IGNORE_TAG(t):
    r'''
    </?(?:PubmedArticleSet|MedlineCitation|DateRevised|PubmedData|History|PubMedPubDate|
    PublicationStatus|ArticleIdList|ArticleId|Journal|JournalIssue|PubDate|Pagination|
    MedlineJournalInfo|CitationSubset|MeshHeadingList|MeshHeading|DescriptorName|
    QualifierName|Initials|AffiliationInfo|Affiliation|PublicationTypeList|
    PublicationType|Country|MedlineTA|NlmUniqueID|ISSNLinking|ISOAbbreviation|PMID)(?: [^>]*)?>
    '''
    return None


def t_DAY(t):
    r'<Day>.*?</Day>'
    return None


def t_MONTH(t):
    r'<Month>.*?</Month>'
    return None


def t_COPYRIGHT_INFORMATION(t):
    r'<CopyrightInformation>.*?</CopyrightInformation>'
    return None  # Retorna None para ignorar o conteúdo


def t_MEDLINEJOURNALINFO(t):
    r'<MedlineJournalInfo>.*?</MedlineJournalInfo>'
    return None


def t_ABSTRACTTEXT_OPEN(t):
    r'<AbstractText(\s+[^>]*)?>'
    return t


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


# Defina uma regra para que seja possível rastrear o números de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


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
