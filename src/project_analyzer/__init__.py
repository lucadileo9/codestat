"""
CodeStat - Project Analyzer
Un tool CLI per analizzare progetti software e generare statistiche dettagliate.
"""

__version__ = "0.1.0"
__author__ = "lucadileo9"
__license__ = "MIT"

from .models import FileStats, DirectoryStats
from .core import ProjectAnalyzer

__all__ = [
    "FileStats",
    "DirectoryStats",
    "ProjectAnalyzer",
    "__version__",
]
