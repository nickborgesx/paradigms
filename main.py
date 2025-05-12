from parser import parser

# Lê o arquivo XML
with open('data/sample.xml', 'r') as f:

    data = f.read()

# Faz o parsing e obtém os artigos
articles = parser.parse(data)

# Mostra os artigos extraídos
for i, art in enumerate(articles, 1):
    print(f"\nArtigo {i}:")
    print(f"  Título:   {art.get('title', [''])[0]}")
    print(f"  Autores:  {', '.join(art.get('author', []))}")
    print(f"  Abstract: {' '.join(art.get('abstract', []))}")
    print(f"  Ano:      {art.get('year', [''])[0]}")
