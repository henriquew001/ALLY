from pygments.lexer import RegexLexer
from pygments.token import *

class MermaidLexer(RegexLexer):
    name = 'Mermaid'
    aliases = ['mermaid']
    filenames = ['*.mermaid']

    tokens = {
        'root': [
            (r'graph\s+([A-Z]{2,3})\b', Keyword),
            (r'([A-Za-z0-9_-]+)(\[.*?\])', bygroups(Name.Label, String)),
            (r'([A-Za-z0-9_-]+)([\(\)\{\}\[\]])', bygroups(Name.Label, Punctuation)),
            (r'--(-+|>|))', Operator),
            (r'(\w+):', Name.Attribute),
            (r'\s+', Text),
        ],
    }
