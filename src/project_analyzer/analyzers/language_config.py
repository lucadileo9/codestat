"""
Configurazione centralizzata per linguaggi di programmazione supportati.
Definisce sintassi dei commenti e mappatura estensioni -> linguaggi.
"""

from typing import Dict, Set
from enum import Enum


class CommentStyle(Enum):
    """Enumerazione che definisce i diversi stili di commento supportati.

    Ogni membro rappresenta una sintassi specifica per i commenti, come quella
    a riga singola (es. `//`, `#`) o multiriga (es. `/* */`).
    """
    """Stili di commento supportati."""
    DOUBLE_SLASH = "//"      # C-style: //
    HASH = "#"               # Python-style: #
    DOUBLE_DASH = "--"       # SQL-style: --
    C_MULTILINE = "/* */"    # C-style multiline: /* */
    HTML = "<!-- -->"        # HTML/XML: <!-- -->


# Configurazione sintassi commenti per linguaggio
# N.B.: usiamo set per evitare duplicati, il che aumenta anche le prestazioni

# q: perché aumenta le prestazioni?
#    - Lookup in set è O(1) vs O(n) in lista
#    - Evita duplicati che richiederebbero controlli aggiuntivi

COMMENT_SYNTAX: Dict[str, Dict[str, Set[CommentStyle]]] = {
    # Linguaggi con // e /* */
    "c_style": {
        "languages": {
            'JavaScript', 'TypeScript', 'C', 'C++', 'C#', 'Java',
            'Kotlin', 'Scala', 'Go', 'Rust', 'Swift', 'Dart', 'PHP', 'Groovy'
        },
        "single_line": {CommentStyle.DOUBLE_SLASH},
        "multi_line": {CommentStyle.C_MULTILINE}
    },
    
    # Linguaggi con #
    "hash_style": {
        "languages": {
            'Python', 'Ruby', 'Shell', 'Bash', 'Zsh', 'Fish',
            'Perl', 'R', 'YAML', 'TOML', 'Elixir'
        },
        "single_line": {CommentStyle.HASH},
        "multi_line": set()  # Nessun commento multi-linea standard
    },
    
    # Linguaggi con --
    "dash_style": {
        "languages": {'SQL', 'Lua', 'Haskell'},
        "single_line": {CommentStyle.DOUBLE_DASH},
        "multi_line": set()
    },
    
    # Linguaggi con <!-- -->
    "markup_style": {
        "languages": {'HTML', 'XML'},
        "single_line": set(),
        "multi_line": {CommentStyle.HTML}
    },
    
    # CSS ha solo multi-linea
    "css_style": {
        "languages": {'CSS', 'SCSS', 'Sass', 'Less'},
        "single_line": set(),
        "multi_line": {CommentStyle.C_MULTILINE}
    }
}


# Mappa estensioni file -> linguaggio
LANGUAGE_MAP: Dict[str, str] = {
    # JavaScript/TypeScript Ecosystem
    '.js': 'JavaScript',
    '.jsx': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript',
    '.mjs': 'JavaScript',
    '.cjs': 'JavaScript',
    
    # Web Frontend
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'Less',
    
    # C Family
    '.c': 'C',
    '.h': 'C',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.hpp': 'C++',
    '.hh': 'C++',
    '.hxx': 'C++',
    '.cs': 'C#',
    
    # Java/JVM Languages
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin',
    '.scala': 'Scala',
    '.groovy': 'Groovy',
    
    # Systems Programming
    '.go': 'Go',
    '.rs': 'Rust',
    '.swift': 'Swift',
    
    # Scripting Languages
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.pl': 'Perl',
    '.lua': 'Lua',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.zsh': 'Zsh',
    '.fish': 'Fish',
    
    # Data & Config
    '.sql': 'SQL',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.xml': 'XML',
    '.toml': 'TOML',
    
    # Statistical & Functional
    '.r': 'R',
    '.R': 'R',
    
    # Apple Ecosystem
    '.m': 'Objective-C',
    '.mm': 'Objective-C++',
    
    # Other Modern Languages
    '.dart': 'Dart',
    '.ex': 'Elixir',
    '.exs': 'Elixir',
    '.erl': 'Erlang',
    '.hrl': 'Erlang',
    '.hs': 'Haskell',
    '.lhs': 'Haskell',
    
    # Editor Languages
    '.vim': 'VimScript',
    '.el': 'EmacsLisp',
    
    # Lisp Family
    '.clj': 'Clojure',
    '.cljs': 'ClojureScript',
    '.lisp': 'CommonLisp',
    '.scm': 'Scheme',
}


class LanguageConfig:
    """
    Helper class per interrogare la configurazione dei linguaggi.
    Fornisce metodi comodi per verificare sintassi e supporto.
    """
    
    def __init__(self):
        """Costruisce un indice invertito per lookup veloce."""
        # Crea mappa linguaggio -> configurazione commenti
        self._language_to_config: Dict[str, Dict] = {}
        
        for style_name, config in COMMENT_SYNTAX.items():
            for lang in config["languages"]:
                self._language_to_config[lang] = {
                    "single_line": config["single_line"],
                    "multi_line": config["multi_line"],
                    "style": style_name
                }
        # _language_to_config: {
        #   'Python': {
        #       "single_line": {CommentStyle.HASH},
        #       "multi_line": set(),
        #       "style": "hash_style"
        #   },
        #   'JavaScript': {
        #       "single_line": {CommentStyle.DOUBLE_SLASH},
        #       ...
        #   }
        # ...
        # Questo permette lookup O(1) per linguaggio, ad esempio
        # 1. _language_to_config["Python"] → trovato subito! O(1)

    def get_single_line_markers(self, language: str) -> Set[str]:
        """Recupera i marcatori per i commenti su riga singola per un dato linguaggio.
        Args:
            language (str): Il nome del linguaggio di programmazione.
        Returns:
            Set[str]: Un insieme di stringhe, dove ogni stringa è un marcatore
                per un commento su riga singola nel linguaggio specificato.
                Restituisce un insieme vuoto se il linguaggio non è trovato o
                non ha marcatori definiti.
        Es.:
            get_single_line_markers("Python") -> {"#"}
            get_single_line_markers("JavaScript") -> {"//"}
            get_single_line_markers("UnknownLang") -> set()
        """
        config = self._language_to_config.get(language, {})
        markers = config.get("single_line", set())
        return {style.value for style in markers}
    
    def get_multi_line_markers(self, language: str) -> Set[str]:
        """
        Ritorna i marker per commenti multi-linea di un linguaggio.
        Args:
            language (str): Il nome del linguaggio di programmazione.
        Returns:
            Set di stringhe (es. {'/* */'}, {'<!-- -->'})
        """
        config = self._language_to_config.get(language, {})
        markers = config.get("multi_line", set())
        return {style.value for style in markers}
    
    def supports_single_line_comments(self, language: str) -> bool:
        """Verifica se il linguaggio supporta commenti singola linea."""
        return len(self.get_single_line_markers(language)) > 0
    
    def supports_multi_line_comments(self, language: str) -> bool:
        """Verifica se il linguaggio supporta commenti multi-linea."""
        return len(self.get_multi_line_markers(language)) > 0
    
    def is_comment_start(self, line: str, language: str) -> bool:
        """
        Verifica se una riga inizia con un marker di commento.
        
        Args:
            line: Riga di codice (già stripped)
            language: Linguaggio del file
            
        Returns:
            True se è un commento
        Es.:
            is_comment_start("# This is a comment", "Python") -> True
            is_comment_start("   // Comment", "JavaScript") -> True
            is_comment_start("let x = 5;", "JavaScript") -> False
        """
        markers = self.get_single_line_markers(language)
        return any(line.startswith(marker) for marker in markers)
    
    def has_multiline_start(self, line: str, language: str) -> tuple[bool, str]:
        """
        Verifica se una riga contiene l'inizio di un commento multi-linea.
        
        Args:
            line: Riga di codice
            language: Linguaggio del file
            
        Returns:
            Tupla (ha_inizio, marker_chiusura)
            Es. (True, '*/') per C-style
        """
        markers = self.get_multi_line_markers(language)
        
        for marker in markers:
            if marker == "/* */":
                if '/*' in line:
                    return True, '*/'
            elif marker == "<!-- -->":
                if '<!--' in line:
                    return True, '-->'
        
        return False, ""
    
    def has_multiline_end(self, line: str, end_marker: str) -> bool:
        """Verifica se una riga contiene la fine di un commento multi-linea."""
        return end_marker in line if end_marker else False


# Istanza singleton per uso globale
language_config = LanguageConfig()
