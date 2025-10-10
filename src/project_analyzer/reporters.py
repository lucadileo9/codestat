"""
Modulo reporters - Formattazione e presentazione dei risultati.
Gestisce l'output su console con formattazione gerarchica e colori.
"""

from .models import DirectoryStats, FileStats


class ConsoleReporter:
    """
    Reporter per output su console con formattazione elegante.
    
    Presenta le statistiche in formato gerarchico con:
    - Emoji per identificare rapidamente i tipi
    - Struttura ad albero per directory
    - Riepilogo finale con percentuali
    - Supporto per modalità verbose/quiet
    """
    
    def __init__(self, verbose: bool = True):
        """
        Inizializza il reporter.
        
        Args:
            verbose: Se True, mostra dettagli per ogni file.
                    Se False, mostra solo statistiche aggregate.
        """
        self.verbose = verbose
    
    def _format_number(self, num: int) -> str:
        """
        Formatta un numero con separatori di migliaia.
        
        Args:
            num: Numero da formattare
            
        Returns:
            Stringa formattata (es: 1,234)
        """
        return f"{num:,}"
    
    def _format_percentage(self, value: float) -> str:
        """
        Formatta una percentuale.
        
        Args:
            value: Valore percentuale
            
        Returns:
            Stringa formattata (es: 72.5%)
        """
        return f"{value:.1f}%"
    
    def print_header(self, project_path: str) -> None:
        """
        Stampa l'intestazione del report.
        
        Args:
            project_path: Path del progetto analizzato
        """
        print()
        print("📊 CodeStat - Project Analysis")
        print("═" * 60)
        print(f"📁 Project: {project_path}")
        print("═" * 60)
        print()
    
    def print_file(self, file_stats: FileStats, indent: int = 0) -> None:
        """
        Stampa le statistiche di un singolo file.
        
        Args:
            file_stats: Statistiche del file
            indent: Livello di indentazione
        """
        prefix = "  " * indent
        
        # Nome file con emoji
        print(f"{prefix}├── 📄 {file_stats.filename}")
        
        # Statistiche base
        stats_line = (
            f"{prefix}│     Lines: {file_stats.total_lines} | "
            f"Code: {file_stats.code_lines} | "
            f"Comments: {file_stats.comment_lines} | "
            f"Blank: {file_stats.blank_lines}"
        )
        print(stats_line)
        
        # Metadati Python se disponibili
        if file_stats.language == "Python" and file_stats.num_classes is not None:
            docstring_icon = "✓" if file_stats.has_docstring else "✗"
            python_line = (
                f"{prefix}│     🐍 Classes: {file_stats.num_classes} | "
                f"Functions: {file_stats.num_functions} | "
                f"Docstring: {docstring_icon}"
            )
            print(python_line)
        elif file_stats.language != "Python":
            # Mostra il linguaggio per file non-Python
            print(f"{prefix}│     Language: {file_stats.language}")
        
        print(f"{prefix}│")
    
    def print_directory(self, dir_stats: DirectoryStats, indent: int = 0, 
                       is_last: bool = True) -> None:
        """
        Stampa ricorsivamente le statistiche di una directory, mostrando anche il numero totale di file e righe.
        
        Args:
            dir_stats: Statistiche della directory
            indent: Livello di indentazione
            is_last: Se questa è l'ultima directory al suo livello
        """
        dir_info = f"({dir_stats.total_files} file, {dir_stats.total_lines} righe)"
        if indent == 0:
            # Root directory
            print(f"📁 {dir_stats.name}/ {dir_info}")
        else:
            prefix = "  " * (indent - 1)
            connector = "└──" if is_last else "├──"
            print(f"{prefix}{connector} 📁 {dir_stats.name}/ {dir_info}")
        # Se verbose, stampa i file
        if self.verbose and dir_stats.files:
            for file_stats in dir_stats.files:
                self.print_file(file_stats, indent)
        # Stampa ricorsivamente le subdirectory
        for i, subdir in enumerate(dir_stats.subdirectories):
            is_last_subdir = (i == len(dir_stats.subdirectories) - 1)
            self.print_directory(subdir, indent + 1, is_last_subdir)
        # Aggiungi riga vuota dopo ogni directory principale
        if indent == 0:
            print()

    def print_directories_only(self, dir_stats: DirectoryStats, indent: int = 0, is_last: bool = True) -> None:
        """
        Stampa solo la struttura delle directory (senza elencare i file), mostrando per ciascuna directory il numero totale di file e righe.
        Args:
            dir_stats: Statistiche della directory
            indent: Livello di indentazione
            is_last: Se questa è l'ultima directory al suo livello
        """
        dir_info = f"({dir_stats.total_files} file, {dir_stats.total_lines} righe)"
        if indent == 0:
            print(f"📁 {dir_stats.name}/ {dir_info}")
        else:
            prefix = "  " * (indent - 1)
            connector = "└──" if is_last else "├──"
            print(f"{prefix}{connector} 📁 {dir_stats.name}/ {dir_info}")
        for i, subdir in enumerate(dir_stats.subdirectories):
            is_last_subdir = (i == len(dir_stats.subdirectories) - 1)
            self.print_directories_only(subdir, indent + 1, is_last_subdir)
        if indent == 0:
            print()

    
    def print_summary(self, stats: DirectoryStats) -> None:
        """
        Stampa il riepilogo finale con statistiche aggregate.
        
        Args:
            stats: Statistiche complete del progetto
        """
        print()
        print("═" * 60)
        print("📈 Summary")
        print("═" * 60)
        print()
        
        # Statistiche generali
        print(f"Total Files: {self._format_number(stats.total_files)}")
        print(f"Total Lines: {self._format_number(stats.total_lines)}")
        
        # Breakdown delle righe
        print(f"  ├── Code: {self._format_number(stats.total_code_lines)} "
              f"({self._format_percentage(stats.code_percentage)})")
        print(f"  ├── Comments: {self._format_number(stats.total_comment_lines)} "
              f"({self._format_percentage(stats.comment_percentage)})")
        print(f"  └── Blank: {self._format_number(stats.total_blank_lines)} "
              f"({self._format_percentage(stats.blank_percentage)})")
        print()
        
        # Statistiche Python se presenti
        python_stats = stats.get_python_stats()
        if python_stats["python_files"] > 0:
            print("🐍 Python Specifics:")
            print(f"  ├── Files: {python_stats['python_files']}")
            print(f"  ├── Classes: {python_stats['num_classes']}")
            print(f"  ├── Functions: {python_stats['num_functions']}")
            print(f"  └── Files with Docstring: {python_stats['files_with_docstring']}")
            print()
        
        print("═" * 60)
        print()
    
    def print_compact_summary(self, stats: DirectoryStats, project_path: str) -> None:
        """
        Stampa un riepilogo compatto (modalità quiet).
        
        Args:
            stats: Statistiche complete del progetto
            project_path: Path del progetto
        """
        print()
        print("📊 CodeStat - Quick Summary")
        print("─" * 40)
        print(f"Project: {project_path}")
        print(f"Files: {self._format_number(stats.total_files)} | "
              f"Lines: {self._format_number(stats.total_lines)}")
        print(f"Code: {self._format_percentage(stats.code_percentage)} | "
              f"Comments: {self._format_percentage(stats.comment_percentage)} | "
              f"Blank: {self._format_percentage(stats.blank_percentage)}")
        
        python_stats = stats.get_python_stats()
        if python_stats["python_files"] > 0:
            print(f"🐍 Python: {python_stats['python_files']} files, "
                  f"{python_stats['num_classes']} classes, "
                  f"{python_stats['num_functions']} functions")
        
        print("─" * 40)
        print()
    
    def report(self, stats: DirectoryStats, project_path: str) -> None:
        """
        Genera il report completo.
        
        Args:
            stats: Statistiche complete del progetto
            project_path: Path del progetto analizzato
        """
        if self.verbose:
            self.print_header(project_path)
            self.print_directory(stats)
            self.print_directories_only(stats)
            self.print_summary(stats)
        else:
            self.print_compact_summary(stats, project_path)


class JSONReporter:
    """
    Reporter per output in formato JSON.
    Utile per integrazione con altri tool o script.
    
    TODO: Implementare in Fase 2
    """
    pass


class HTMLReporter:
    """
    Reporter per generare report HTML con grafici.
    
    TODO: Implementare in Fase 3
    """
    pass
