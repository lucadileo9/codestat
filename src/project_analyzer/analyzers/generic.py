"""
Analyzer generico per linguaggi di programmazione comuni.
Usa configurazione centralizzata per identificare commenti e codice.
"""

from pathlib import Path
from typing import Set
from .base import BaseAnalyzer
from .language_config import LANGUAGE_MAP, language_config
from ..models import FileStats


class GenericAnalyzer(BaseAnalyzer):
    """
    Analyzer generico che supporta la maggior parte dei linguaggi comuni.
    
    Utilizza la configurazione centralizzata in language_config.py per:
    - Riconoscere estensioni file
    - Identificare sintassi dei commenti
    - Gestire commenti singola e multi-linea
    
    Supporta linguaggi con:
    - // per commenti singola linea (C, C++, Java, JavaScript, Go, Rust, etc.)
    - # per commenti singola linea (Python, Ruby, Shell, etc.)
    - /* */ per commenti multi-linea (C, C++, Java, JavaScript, CSS, etc.)
    - <!-- --> per HTML/XML
    - -- per SQL, Lua, Haskell
    """
    
    @property
    def supported_extensions(self) -> Set[str]:
        """Tutte le estensioni supportate dall'analyzer generico."""
        return set(LANGUAGE_MAP.keys())
    
    @property
    def language_name(self) -> str:
        """Nome generico dell'analyzer."""
        return "Generic"
    
    def _get_language_for_file(self, file_path: Path) -> str:
        """Determina il linguaggio dal path del file."""
        ext = file_path.suffix.lower()
        return LANGUAGE_MAP.get(ext, "Unknown")
    
    
    def analyze(self, file_path: Path) -> FileStats:
        """
        Analizza un file generico e ritorna le statistiche.
        
        Args:
            file_path: Path del file da analizzare
            
        Returns:
            FileStats con le statistiche del file
        """
        language = self._get_language_for_file(file_path)
        total_lines, blank_lines, lines = self._count_lines(file_path)
        
        if total_lines == 0:
            return FileStats(
                path=file_path,
                total_lines=0,
                code_lines=0,
                comment_lines=0,
                blank_lines=0,
                language=language
            )
        
        # Conta righe di commento
        comment_lines = 0  
        # flag booleano per tracciare se siamo dentro un commento multi-linea
        in_multiline_comment = False
        # stringa che indica come chiudere il commento multi-linea corrente
        multiline_end_marker = ""
        
        for line in lines:
            stripped = line.strip()
            
            # Salta righe vuote (già contate)
            if not stripped:
                continue
            
            # Gestione commenti multi-linea
            if language_config.supports_multi_line_comments(language):
                # Siamo già dentro un commento multi-linea?
                if in_multiline_comment:
                    # allora aumentiamo il contatore
                    comment_lines += 1
                    # Se troviamo la fine del commento multi-linea, usciamo
                    if language_config.has_multiline_end(stripped, multiline_end_marker):
                        # resetta lo stato
                        in_multiline_comment = False 
                        multiline_end_marker = ""
                    continue
                
                # Inizia un commento multi-linea?
                has_start, end_marker = language_config.has_multiline_start(stripped, language)
                if has_start:
                    comment_lines += 1
                    # Se non finisce sulla stessa riga, entriamo in modalità multi-linea
                    if not language_config.has_multiline_end(stripped, end_marker):
                        in_multiline_comment = True
                        multiline_end_marker = end_marker
                    continue
            
            # Commenti singola linea
            if language_config.is_comment_start(stripped, language):
                comment_lines += 1
                continue
        
        # Calcola righe di codice
        code_lines = total_lines - blank_lines - comment_lines
        
        return FileStats(
            path=file_path,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            language=language
        )
