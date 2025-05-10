from parser import parser, articles

# Lê o arquivo XML
with open('sample.xml', 'r') as f:
    data = f.read()

# Faz o parsing
parser.parse(data)

# Mostra os artigos extraídos
for i, art in enumerate(articles, 1):
    print(f"\nArtigo {i}:")
    print(f"  Título:   {art.get('title', [''])[0]}")
    print(f"  Autores:  {', '.join(art.get('author', []))}")
    print(f"  Abstract: {art.get('abstract', [''])[0]}")
    print(f"  Ano:      {art.get('year', [''])[0]}")
