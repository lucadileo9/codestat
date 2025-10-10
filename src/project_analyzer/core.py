"""
Modulo core - Logica principale per l'analisi dei progetti.
Coordina gli analyzer e gestisce la scansione ricorsiva delle directory.
"""

from pathlib import Path
from typing import List, Set, Optional
from .models import FileStats, DirectoryStats
from .analyzers import PythonAnalyzer, GenericAnalyzer, BaseAnalyzer


class ProjectAnalyzer:
    """
    Classe principale per analizzare progetti software.
    
    Responsabilità:
    - Scansione ricorsiva delle directory
    - Selezione dell'analyzer appropriato per ogni file
    - Filtraggio di directory e file da ignorare
    - Costruzione della struttura DirectoryStats
    """
    
    # Directory da ignorare sempre
    IGNORED_DIRS = {
        # Python
        'venv', 'env', '.venv', '__pycache__', '.eggs', 'build', 'dist',
        '*.egg-info', '.pytest_cache', '.tox', '.mypy_cache',
        
        # Node.js
        'node_modules', '.npm',
        
        # Version Control
        '.git', '.svn', '.hg', '.bzr',
        
        # IDEs
        '.idea', '.vscode', '.vs', '.eclipse', '.settings',
        
        # Build artifacts
        'target', 'out', 'bin', 'obj',
        
        # Misc
        '.cache', 'tmp', 'temp', 'logs', 'coverage',
    }
    
    # File da ignorare (pattern comuni)
    IGNORED_FILES = {
        '.DS_Store', 'Thumbs.db', '.gitignore', '.dockerignore',
        '*.pyc', '*.pyo', '*.so', '*.dll', '*.dylib',
        '*.class', '*.jar', '*.war',
        '*.min.js', '*.min.css',
    }
    
    def __init__(self, 
                 root_path: Path,
                 file_extensions: Optional[Set[str]] = None,
                 ignore_dirs: Optional[Set[str]] = None):
        """
        Inizializza l'analyzer.
        
        Args:
            root_path: Directory radice del progetto da analizzare
            file_extensions: Set di estensioni da analizzare (es: {'.py', '.js'})
                            Se None, analizza tutti i file supportati
            ignore_dirs: Directory aggiuntive da ignorare
        """
        self.root_path = Path(root_path).resolve()
        self.file_extensions = file_extensions
        self.ignore_dirs = self.IGNORED_DIRS.copy()
        
        if ignore_dirs:
            self.ignore_dirs.update(ignore_dirs)
        
        # Inizializza gli analyzer
        self.analyzers: List[BaseAnalyzer] = [
            PythonAnalyzer(),
            GenericAnalyzer(),
        ]
    
    def _should_ignore_dir(self, dir_path: Path) -> bool:
        """
        Determina se una directory dovrebbe essere ignorata.
        
        Args:
            dir_path: Path della directory da controllare
            
        Returns:
            True se la directory deve essere ignorata
        """
        dir_name = dir_path.name
        
        # Controlla se il nome della directory è nella lista di ignore
        if dir_name in self.ignore_dirs:
            return True
        
        # Controlla directory nascoste (che iniziano con .)
        if dir_name.startswith('.') and dir_name not in {'.', '..'}:
            return True
        
        return False
    
    def _should_analyze_file(self, file_path: Path) -> bool:
        """
        Determina se un file dovrebbe essere analizzato.
        
        Args:
            file_path: Path del file da controllare
            
        Returns:
            True se il file deve essere analizzato
        """
        # Ignora file nascosti
        if file_path.name.startswith('.'):
            return False
        
        # Se sono specificate estensioni, filtra solo quelle
        if self.file_extensions:
            return file_path.suffix.lower() in self.file_extensions
        
        # Altrimenti, controlla se almeno un analyzer lo supporta
        return any(analyzer.can_analyze(file_path) for analyzer in self.analyzers)
    
    def _get_analyzer_for_file(self, file_path: Path) -> Optional[BaseAnalyzer]:
        """
        Trova l'analyzer appropriato per un file.
        
        Args:
            file_path: Path del file
            
        Returns:
            L'analyzer appropriato o None se nessuno è disponibile
        """
        # Prova prima gli analyzer specifici (Python ha priorità)
        for analyzer in self.analyzers:
            if analyzer.can_analyze(file_path):
                return analyzer
        
        return None
    
    def _analyze_file(self, file_path: Path) -> Optional[FileStats]:
        """
        Analizza un singolo file.
        
        Args:
            file_path: Path del file da analizzare
            
        Returns:
            FileStats o None se l'analisi fallisce
        """
        analyzer = self._get_analyzer_for_file(file_path)
        
        if not analyzer:
            return None
        
        try:
            return analyzer.analyze(file_path)
        except Exception as e:
            # Log dell'errore (in futuro si potrebbe usare logging)
            print(f"Warning: Failed to analyze {file_path}: {e}")
            return None
    
    def _analyze_directory(self, dir_path: Path) -> DirectoryStats:
        """
        Analizza ricorsivamente una directory.
        
        Args:
            dir_path: Path della directory da analizzare
            
        Returns:
            DirectoryStats con tutte le statistiche
        """
        dir_stats = DirectoryStats(path=dir_path)
        
        try:
            # Ottieni tutti gli elementi nella directory
            items = sorted(dir_path.iterdir())
        except PermissionError:
            # Se non abbiamo permessi, ritorna statistiche vuote
            return dir_stats
        
        for item in items:
            if item.is_file():
                # Analizza il file se appropriato
                if self._should_analyze_file(item):
                    file_stats = self._analyze_file(item)
                    if file_stats:
                        dir_stats.files.append(file_stats)
            
            elif item.is_dir():
                # Analizza ricorsivamente la subdirectory se non ignorata
                if not self._should_ignore_dir(item):
                    subdir_stats = self._analyze_directory(item)
                    # Aggiungi solo se contiene file analizzati
                    if subdir_stats.total_files > 0:
                        dir_stats.subdirectories.append(subdir_stats)
        
        return dir_stats
    
    def analyze(self) -> DirectoryStats:
        """
        Analizza l'intero progetto dalla root.
        
        Returns:
            DirectoryStats con le statistiche complete del progetto
            
        Raises:
            FileNotFoundError: Se il path root non esiste
            NotADirectoryError: Se il path root non è una directory
        """
        if not self.root_path.exists():
            raise FileNotFoundError(f"Path does not exist: {self.root_path}")
        
        if not self.root_path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.root_path}")
        
        # Analizza dalla root
        stats = self._analyze_directory(self.root_path)
        
        # Ordina i file per dimensione
        stats.sort_files_by_size()
        
        return stats
    
    def get_supported_extensions(self) -> Set[str]:
        """
        Ritorna tutte le estensioni supportate dagli analyzer disponibili.
        
        Returns:
            Set di estensioni file supportate
        """
        extensions = set()
        for analyzer in self.analyzers:
            extensions.update(analyzer.supported_extensions)
        return extensions
