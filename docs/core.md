# Modulo core: ProjectAnalyzer

Questa pagina documenta la classe `ProjectAnalyzer` e le sue funzionalità principali, che costituiscono il cuore logico dell'analisi dei progetti in `codestat`.

## Scopo del modulo

Il modulo `core.py` fornisce la logica centrale per l'analisi ricorsiva di progetti software. Coordina gli analyzer specifici per linguaggio, gestisce la scansione delle directory e costruisce la struttura dati delle statistiche del progetto.

## Flusso di Analisi

Il seguente diagramma illustra il flusso completo dell'analisi del progetto:

```mermaid
flowchart TD
    Start([Inizio Analisi]) --> Init[ProjectAnalyzer inizializzato<br/>con root_path]
    Init --> AnalyzeCall[analyze chiamato]
    AnalyzeCall --> CheckRoot{Root path<br/>valido?}
    
    CheckRoot -->|No| Error[Solleva FileNotFoundError/<br/>NotADirectoryError]
    CheckRoot -->|Yes| AnalyzeDir[_analyze_directory root]

    
    IterItems -->|Finito| SortFiles[sort_files_by_size]
    SortFiles --> Return[Ritorna DirectoryStats]
    Return --> End([Fine])
    
    AnalyzeDir --> GetItems[Ottieni elementi<br/>in directory]
    GetItems --> IterItems{Per ogni<br/>elemento}
    
    IterItems --> CheckType{Tipo?}
    CheckType -->|Directory| ShouldIgnore{_should_ignore_dir?}
    CheckType -->|File| ShouldAnalyze{_should_analyze_file?}
    
    ShouldAnalyze -->|Yes| GetAnalyzer[_get_analyzer_for_file]
    ShouldAnalyze -->|No| IterItems
    
    GetAnalyzer --> RunAnalyzer[analyzer.analyze]
    RunAnalyzer --> AddFile[Aggiungi FileStats<br/>a dir_stats.files]
    AddFile --> IterItems
    
    ShouldIgnore -->|No| RecursiveCall[_analyze_directory<br/>ricorsivo]
    ShouldIgnore -->|Yes| IterItems
    
    RecursiveCall --> AddSubdir{Subdirectory<br/>ha file?}
    AddSubdir -->|Yes| AddToList[Aggiungi a<br/>dir_stats.subdirectories]
    AddSubdir -->|No| IterItems
    AddToList --> IterItems
    
    
    style Start fill:#086e08
    style End fill:#cf0e2b
    style Error fill:#ab2b2b
    style RecursiveCall fill:#387f9c
```

## Classe principale: `ProjectAnalyzer`

### Responsabilità
- Scansione ricorsiva delle directory di progetto
- Selezione automatica dell'analyzer più adatto per ogni file
- Filtraggio di directory e file da ignorare (es. build, cache, VCS, ecc.)
- Costruzione della struttura ad albero delle statistiche (`DirectoryStats`)

### Inizializzazione
```python
ProjectAnalyzer(
    root_path: Path,
    file_extensions: Optional[Set[str]] = None,
    ignore_dirs: Optional[Set[str]] = None
)
```
- **root_path**: directory radice del progetto da analizzare
- **file_extensions**: set di estensioni da considerare (es. `{'.py', '.js'}`), opzionale
- **ignore_dirs**: directory aggiuntive da ignorare, opzionale

### Metodi principali

#### `analyze()`
Analizza ricorsivamente il progetto a partire dalla root, restituendo una struttura `DirectoryStats` con tutte le statistiche raccolte.

#### `get_supported_extensions()`
Restituisce l'insieme delle estensioni file supportate dagli analyzer disponibili.

### Filtri e regole di esclusione
- Directory ignorate: vedi costante `IGNORED_DIRS` (es. `venv`, `.git`, `node_modules`, ecc.)
- File ignorati: vedi costante `IGNORED_FILES` (es. `.DS_Store`, `*.pyc`, ecc.)
- File nascosti e directory nascoste vengono esclusi automaticamente

### Selezione degli analyzer
Il modulo utilizza una lista di analyzer (es. `PythonAnalyzer`, `GenericAnalyzer`) e seleziona automaticamente quello più adatto per ogni file tramite il metodo `can_analyze`.

#### Diagramma di Selezione Analyzer

```mermaid
sequenceDiagram
    participant PA as ProjectAnalyzer
    participant File as File Path
    participant PY as PythonAnalyzer
    participant MD as MarkdownAnalyzer
    participant GEN as GenericAnalyzer
    
    PA->>File: _get_analyzer_for_file(file_path)
    
    PA->>PY: can_analyze(file_path)?
    PY-->>PA: Check .py, .pyw, .pyi
    
    alt File is Python
        PY-->>PA: True
        PA->>PY: analyze(file_path)
        PY-->>PA: FileStats (con AST info)
    else Not Python
        PA->>MD: can_analyze(file_path)?
        MD-->>PA: Check .md, .markdown
        
        alt File is Markdown
            MD-->>PA: True
            PA->>MD: analyze(file_path)
            MD-->>PA: FileStats (con Markdown stats)
        else Not Markdown
            PA->>GEN: can_analyze(file_path)?
            GEN-->>PA: True (supporta tutto)
            PA->>GEN: analyze(file_path)
            GEN-->>PA: FileStats (analisi base)
        end
    end
```

### Esempio d'uso
```python
from project_analyzer.core import ProjectAnalyzer
from pathlib import Path

analyzer = ProjectAnalyzer(root_path=Path('.'))
stats = analyzer.analyze()
print(stats.summary())
```

## Dipendenze
- `project_analyzer.models` (FileStats, DirectoryStats)
- `project_analyzer.analyzers` (PythonAnalyzer, GenericAnalyzer, BaseAnalyzer)

## Note
- In caso di errori nell'analisi di un file, viene stampato un warning ma l'analisi prosegue.
- Le statistiche finali sono ordinate per dimensione dei file.

---

Per dettagli sulle statistiche e i modelli dati, vedi la documentazione di [`models.md`](models.md).
