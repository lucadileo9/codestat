"""
Modelli dati per le statistiche dei file e delle directory.
Utilizza dataclasses per strutture immutabili e tipo-safe.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path


@dataclass
class FileStats:
    """
    Statistiche per un singolo file.
    
    Attributes:
        path: Percorso del file
        total_lines: Numero totale di righe nel file
        code_lines: Righe contenenti codice effettivo
        comment_lines: Righe di commento
        blank_lines: Righe vuote o con solo spazi
        language: Linguaggio di programmazione rilevato
        has_docstring: (Python) Se il modulo ha docstring
        num_classes: (Python) Numero di classi definite
        num_functions: (Python) Numero di funzioni/metodi definiti
    """
    path: Path
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    language: str = "unknown"
    
    # Metadati specifici per Python
    has_docstring: Optional[bool] = None
    num_classes: Optional[int] = None
    num_functions: Optional[int] = None
    
    @property
    def filename(self) -> str:
        """Ritorna il nome del file."""
        return self.path.name
    
    @property
    def code_percentage(self) -> float:
        """Calcola la percentuale di righe di codice."""
        if self.total_lines == 0:
            return 0.0
        return (self.code_lines / self.total_lines) * 100
    
    @property
    def comment_percentage(self) -> float:
        """Calcola la percentuale di commenti."""
        if self.total_lines == 0:
            return 0.0
        return (self.comment_lines / self.total_lines) * 100
    
    def __str__(self) -> str:
        """Rappresentazione stringa leggibile."""
        return (
            f"{self.filename}: {self.total_lines} lines "
            f"({self.code_lines} code, {self.comment_lines} comments, "
            f"{self.blank_lines} blank)"
        )


@dataclass
class DirectoryStats:
    """
    Statistiche per una directory, includendo file e subdirectory.
    
    Attributes:
        path: Percorso della directory
        files: Lista di FileStats per i file nella directory
        subdirectories: Lista di DirectoryStats per le sottodirectory
    """
    path: Path
    files: List[FileStats] = field(default_factory=list)
    subdirectories: List['DirectoryStats'] = field(default_factory=list)
    
    @property
    def name(self) -> str:
        """Ritorna il nome della directory."""
        return self.path.name if self.path.name else str(self.path)
    
    @property
    def total_files(self) -> int:
        """Conta ricorsivamente tutti i file."""
        count = len(self.files)
        for subdir in self.subdirectories:
            count += subdir.total_files
        return count
    
    @property
    def total_lines(self) -> int:
        """Somma ricorsivamente tutte le righe."""
        total = sum(f.total_lines for f in self.files)
        for subdir in self.subdirectories:
            total += subdir.total_lines
        return total
    
    @property
    def total_code_lines(self) -> int:
        """Somma ricorsivamente tutte le righe di codice."""
        total = sum(f.code_lines for f in self.files)
        for subdir in self.subdirectories:
            total += subdir.total_code_lines
        return total
    
    @property
    def total_comment_lines(self) -> int:
        """Somma ricorsivamente tutte le righe di commento."""
        total = sum(f.comment_lines for f in self.files)
        for subdir in self.subdirectories:
            total += subdir.total_comment_lines
        return total
    
    @property
    def total_blank_lines(self) -> int:
        """Somma ricorsivamente tutte le righe vuote."""
        total = sum(f.blank_lines for f in self.files)
        for subdir in self.subdirectories:
            total += subdir.total_blank_lines
        return total
    
    @property
    def code_percentage(self) -> float:
        """Calcola la percentuale di codice sul totale."""
        if self.total_lines == 0:
            return 0.0
        return (self.total_code_lines / self.total_lines) * 100
    
    @property
    def comment_percentage(self) -> float:
        """Calcola la percentuale di commenti sul totale."""
        if self.total_lines == 0:
            return 0.0
        return (self.total_comment_lines / self.total_lines) * 100
    
    @property
    def blank_percentage(self) -> float:
        """Calcola la percentuale di righe vuote sul totale."""
        if self.total_lines == 0:
            return 0.0
        return (self.total_blank_lines / self.total_lines) * 100
    
    def get_python_stats(self) -> dict:
        """
        Ritorna statistiche aggregate specifiche per Python.
        
        Returns:
            Dict con num_classes, num_functions, files_with_docstring
        """
        total_classes = 0
        total_functions = 0
        files_with_docstring = 0
        python_files = 0
        
        # Raccoglie statistiche dai file in questa directory
        for file_stat in self.files:
            if file_stat.language.lower() == "python":
                python_files += 1
                if file_stat.num_classes is not None:
                    total_classes += file_stat.num_classes
                if file_stat.num_functions is not None:
                    total_functions += file_stat.num_functions
                if file_stat.has_docstring:
                    files_with_docstring += 1
        
        # Raccoglie ricorsivamente dalle subdirectory
        for subdir in self.subdirectories:
            subdir_stats = subdir.get_python_stats()
            total_classes += subdir_stats["num_classes"]
            total_functions += subdir_stats["num_functions"]
            files_with_docstring += subdir_stats["files_with_docstring"]
            python_files += subdir_stats["python_files"]
        
        return {
            "num_classes": total_classes,
            "num_functions": total_functions,
            "files_with_docstring": files_with_docstring,
            "python_files": python_files,
        }
    
    def sort_files_by_size(self) -> None:
        """Ordina i file per numero di righe (dal più grande al più piccolo)."""
        self.files.sort(key=lambda f: f.total_lines, reverse=True)
        
        # Ordina ricorsivamente anche le subdirectory
        for subdir in self.subdirectories:
            subdir.sort_files_by_size()
    
    def __str__(self) -> str:
        """Rappresentazione stringa leggibile."""
        return (
            f"{self.name}: {self.total_files} files, {self.total_lines} lines "
            f"({self.total_code_lines} code, {self.total_comment_lines} comments, "
            f"{self.total_blank_lines} blank)"
        )
