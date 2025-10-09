"""
Analyzer specifico per Python usando Abstract Syntax Tree (AST).
Fornisce analisi profonda del codice senza eseguirlo.
"""

import ast
import tokenize
from pathlib import Path
from typing import Set, List
from io import StringIO
from .base import BaseAnalyzer
from ..models import FileStats


class PythonAnalyzer(BaseAnalyzer):
    """
    Analyzer specializzato per codice Python.
    
    Usa l'AST (Abstract Syntax Tree) per:
    - Rilevare docstring a livello di modulo
    - Contare classi definite
    - Contare funzioni e metodi
    - Distinguere accuratamente codice da commenti
    
    Usa il modulo tokenize per:
    - Identificare con precisione i commenti (inclusi inline)
    - Gestire correttamente stringhe multi-linea
    """
    
    @property
    def supported_extensions(self) -> Set[str]:
        """Estensioni Python supportate."""
        return {'.py', '.pyw', '.pyi'}
    
    @property
    def language_name(self) -> str:
        """Nome del linguaggio."""
        return "Python"
    
    def _extract_ast_info(self, file_path: Path) -> tuple:
        """
        Estrae informazioni usando AST.
        
        Args:
            file_path: Path del file Python
            
        Returns:
            Tupla (has_docstring, num_classes, num_functions)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Parse l'AST
            tree = ast.parse(source, filename=str(file_path))
            
            # Estrai docstring del modulo
            has_docstring = ast.get_docstring(tree) is not None
            
            # Conta classi e funzioni
            num_classes = 0
            num_functions = 0
            
            # walk è una funzione comoda per visitare tutti i nodi
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    num_classes += 1
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    num_functions += 1
            
            return has_docstring, num_classes, num_functions
            
        except (SyntaxError, UnicodeDecodeError):
            # Se il file ha errori di sintassi o encoding, ritorna valori di default
            return False, 0, 0
        except Exception:
            return False, 0, 0
    
    def _count_comment_lines(self, file_path: Path) -> int:
        """
        Conta le righe di commento usando il tokenizer Python.
        Questo è più accurato del pattern matching perché gestisce:
        - Commenti inline
        - Stringhe multi-linea che non sono docstring
        - Edge cases complessi
        
        Args:
            file_path: Path del file Python
            
        Returns:
            Numero di righe contenenti commenti
        """
        try:
            # N.B.: tokenize richiede un file aperto in modalità binaria
            with open(file_path, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                comment_lines = set()
                
                for tok in tokens: # per ogni token generato
                    if tok.type == tokenize.COMMENT: # se è un commento
                        comment_lines.add(tok.start[0]) # aggiungi il numero di riga
                
                return len(comment_lines)
                
        except (tokenize.TokenError, UnicodeDecodeError):
            # Fallback: conta commenti con pattern semplice
            return self._count_comment_lines_simple(file_path)
        except Exception:
            return 0
    
    def _count_comment_lines_simple(self, file_path: Path) -> int:
        """
        Fallback semplice per contare commenti se il tokenizer fallisce.
        
        Args:
            file_path: Path del file Python
            
        Returns:
            Numero di righe con commenti
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            comment_count = 0
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    comment_count += 1
            
            return comment_count
            
        except Exception:
            return 0
    
    def _is_docstring_line(self, line: str) -> bool:
        """
        Determina se una riga contiene parte di una docstring.
        Questo è un controllo semplificato.
        
        Args:
            line: Riga da verificare
            
        Returns:
            True se sembra essere parte di una docstring
        """
        stripped = line.strip()
        # Controlla se inizia con triple quotes
        return (stripped.startswith('"""') or 
                stripped.startswith("'''") or
                stripped.endswith('"""') or
                stripped.endswith("'''"))
    
    def analyze(self, file_path: Path) -> FileStats:
        """
        Analizza un file Python e ritorna statistiche dettagliate.
        
        Args:
            file_path: Path del file Python da analizzare
            
        Returns:
            FileStats con statistiche complete inclusi metadati Python
        """
        # Conteggio base delle righe
        total_lines, blank_lines, lines = self._count_lines(file_path)
        
        if total_lines == 0:
            return FileStats(
                path=file_path,
                total_lines=0,
                code_lines=0,
                comment_lines=0,
                blank_lines=0,
                language="Python",
                has_docstring=False,
                num_classes=0,
                num_functions=0
            )
        
        # Estrai informazioni AST
        has_docstring, num_classes, num_functions = self._extract_ast_info(file_path)
        
        # Conta commenti con tokenizer
        comment_lines = self._count_comment_lines(file_path)
        
        # Stima righe di codice
        # Nota: questa è una stima perché docstring multi-linea
        # possono essere sia documentazione che codice
        code_lines = total_lines - blank_lines - comment_lines
        
        # Assicurati che i valori siano sensati
        if code_lines < 0:
            code_lines = 0
        
        return FileStats(
            path=file_path,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            language="Python",
            has_docstring=has_docstring,
            num_classes=num_classes,
            num_functions=num_functions
        )