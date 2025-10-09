"""
Classe base astratta per tutti gli analyzer.
Definisce l'interfaccia comune che ogni analyzer deve implementare (Strategy Pattern).
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Set
from ..models import FileStats


class BaseAnalyzer(ABC):
    """
    Classe astratta per analizzare file di codice.
    
    Ogni analyzer concreto deve:
    1. Definire le estensioni supportate
    2. Implementare il metodo analyze() per il proprio linguaggio
    """
    
    @property
    @abstractmethod
    def supported_extensions(self) -> Set[str]:
        """
        Ritorna il set di estensioni file supportate dall'analyzer.
        
        Returns:
            Set di estensioni (es: {'.py', '.pyw'})
        """
        pass
    
    @property
    @abstractmethod
    def language_name(self) -> str:
        """
        Nome del linguaggio gestito dall'analyzer.
        
        Returns:
            Nome del linguaggio (es: "Python", "JavaScript")
        """
        pass
    
    def can_analyze(self, file_path: Path) -> bool:
        """
        Determina se questo analyzer può analizzare il file specificato.
        
        Args:
            file_path: Path del file da verificare
            
        Returns:
            True se l'analyzer supporta questo tipo di file
        """
        return file_path.suffix.lower() in self.supported_extensions
    
    @abstractmethod
    def analyze(self, file_path: Path) -> FileStats:
        """
        Analizza un file e ritorna le statistiche.
        
        Args:
            file_path: Path del file da analizzare
            
        Returns:
            FileStats con le statistiche del file
            
        Raises:
            FileNotFoundError: Se il file non esiste
            PermissionError: Se non ci sono permessi di lettura
            UnicodeDecodeError: Se il file non può essere decodificato
        """
        pass
    
    def _count_lines(self, file_path: Path, encoding: str = 'utf-8') -> tuple:
        """
        Helper method per contare le righe base di un file.
        
        Args:
            file_path: Path del file
            encoding: Encoding da utilizzare per leggere il file
            
        Returns:
            Tupla (total_lines, blank_lines, lines_content)
            dove 
            - lines_content è la lista delle righe del file
            - total_lines è il numero totale di righe
            - blank_lines è il numero di righe vuote
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Prova con encoding diverso se UTF-8 fallisce
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
            except Exception:
                # Se anche questo fallisce, ritorna valori di default
                return 0, 0, []
        except Exception:
            return 0, 0, []
        
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if line.strip() == '')
        
        return total_lines, blank_lines, lines
