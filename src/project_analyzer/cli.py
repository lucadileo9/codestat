"""
Modulo CLI - Interfaccia a riga di comando per CodeStat.
Gestisce argomenti, opzioni e coordinamento tra core e reporter.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List
from . import __version__
from .core import ProjectAnalyzer
from .reporters import ConsoleReporter


def create_parser() -> argparse.ArgumentParser:
    """
    Crea e configura l'argument parser per la CLI.
    
    Returns:
        ArgumentParser configurato
    """
    parser = argparse.ArgumentParser(
        prog='codestat',
        description='📊 Analizza progetti software e genera statistiche dettagliate',
        epilog='Per maggiori informazioni: https://github.com/lucadileo9/codestat',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Argomento posizionale: path del progetto
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path del progetto da analizzare (default: directory corrente)'
    )
    
    # Opzioni per filtrare i file
    parser.add_argument(
        '-e', '--ext',
        action='append',
        dest='extensions',
        metavar='EXT',
        help='Estensioni file da analizzare (es: --ext .py --ext .js). '
             'Se non specificato, analizza tutti i file supportati.'
    )
    
    # Opzioni per ignorare directory
    parser.add_argument(
        '-i', '--ignore',
        action='append',
        dest='ignore_dirs',
        metavar='DIR',
        help='Directory aggiuntive da ignorare (es: --ignore build --ignore temp)'
    )
    
    # Opzioni di output
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Mostra solo il riepilogo senza dettagli dei file'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Output dettagliato (default)'
    )
    
    # Opzioni informative
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '--list-extensions',
        action='store_true',
        help='Mostra tutte le estensioni supportate ed esce'
    )
    
    return parser


def list_supported_extensions() -> None:
    """Stampa tutte le estensioni file supportate."""
    analyzer = ProjectAnalyzer(Path('.'))
    extensions = sorted(analyzer.get_supported_extensions())
    
    print()
    print("📋 Estensioni Supportate:")
    print("═" * 40)
    
    # Raggruppa per categoria (approssimativa)
    categories = {
        'Python': ['.py', '.pyw', '.pyi'],
        'JavaScript/TypeScript': ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'],
        'Web': ['.html', '.htm', '.css', '.scss', '.sass', '.less'],
        'C/C++': ['.c', '.h', '.cpp', '.cc', '.cxx', '.hpp', '.hh', '.hxx'],
        'Java/JVM': ['.java', '.kt', '.kts', '.scala', '.groovy'],
        'Altri': []
    }
    
    # Categorizza le estensioni
    categorized = set()
    for category, exts in categories.items():
        matching = [e for e in extensions if e in exts]
        if matching:
            print(f"\n{category}:")
            print(f"  {', '.join(matching)}")
            categorized.update(matching)
    
    # Estensioni non categorizzate
    others = [e for e in extensions if e not in categorized]
    if others:
        print(f"\nAltri linguaggi:")
        # Stampa in colonne
        cols = 6
        for i in range(0, len(others), cols):
            chunk = others[i:i+cols]
            print(f"  {', '.join(chunk)}")
    
    print()
    print(f"Totale: {len(extensions)} estensioni supportate")
    print("═" * 40)
    print()


def validate_path(path_str: str) -> Path:
    """
    Valida e converte una stringa path in Path object.
    
    Args:
        path_str: Stringa del path
        
    Returns:
        Path object validato
        
    Raises:
        SystemExit: Se il path non è valido
    """
    path = Path(path_str).resolve()
    
    if not path.exists():
        print(f"❌ Errore: Il path '{path}' non esiste.", file=sys.stderr)
        sys.exit(1)
    
    if not path.is_dir():
        print(f"❌ Errore: Il path '{path}' non è una directory.", file=sys.stderr)
        sys.exit(1)
    
    return path


def parse_extensions(extensions: Optional[List[str]]) -> Optional[set]:
    """
    Processa e valida le estensioni specificate dall'utente.
    
    Args:
        extensions: Lista di estensioni dalla CLI
        
    Returns:
        Set di estensioni normalizzate o None
    """
    if not extensions:
        return None
    
    # Normalizza le estensioni (aggiungi . se mancante)
    normalized = set()
    for ext in extensions:
        if not ext.startswith('.'):
            ext = '.' + ext
        normalized.add(ext.lower())
    
    return normalized


def main() -> int:
    """
    Entry point principale della CLI.
    
    Returns:
        Exit code (0 per successo, 1 per errore)
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Gestisci --list-extensions
    if args.list_extensions:
        list_supported_extensions()
        return 0
    
    # Valida il path
    try:
        project_path = validate_path(args.path)
    except SystemExit as e:
        return e.code
    
    # Processa le estensioni
    extensions = parse_extensions(args.extensions)
    
    # Determina la verbosità (default: verbose)
    verbose = not args.quiet
    
    # Stampa messaggio iniziale
    if verbose:
        print("🔍 Analyzing project...")
        print(f"   Path: {project_path}")
        if extensions:
            print(f"   Extensions: {', '.join(sorted(extensions))}")
        print()
    
    # Crea l'analyzer
    try:
        analyzer = ProjectAnalyzer(
            root_path=project_path,
            file_extensions=extensions,
            ignore_dirs=set(args.ignore_dirs) if args.ignore_dirs else None
        )
    except Exception as e:
        print(f"❌ Errore nell'inizializzazione: {e}", file=sys.stderr)
        return 1
    
    # Esegui l'analisi
    try:
        stats = analyzer.analyze()
    except Exception as e:
        print(f"❌ Errore durante l'analisi: {e}", file=sys.stderr)
        return 1
    
    # Verifica se ci sono file analizzati
    if stats.total_files == 0:
        print("⚠️  Nessun file analizzato.")
        print("   Suggerimenti:")
        print("   - Verifica che la directory contenga file di codice")
        print("   - Usa --ext per specificare estensioni particolari")
        print("   - Usa --list-extensions per vedere i tipi supportati")
        return 0
    
    # Genera il report
    reporter = ConsoleReporter(verbose=verbose)
    reporter.report(stats, str(project_path))
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
