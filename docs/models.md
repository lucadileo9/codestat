# 📦 Models - Strutture Dati

Definisce le strutture dati per rappresentare statistiche di file e directory.

---

## 📄 FileStats

**Rappresenta le statistiche di un singolo file.**

### Attributi

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `path` | `Path` | Percorso assoluto del file |
| `total_lines` | `int` | Righe totali (codice + commenti + vuote) |
| `code_lines` | `int` | Solo righe con codice effettivo |
| `comment_lines` | `int` | Solo righe di commento |
| `blank_lines` | `int` | Righe vuote o con solo spazi |
| `language` | `str` | Linguaggio rilevato (es. "Python", "JavaScript") |

#### Metadati Python (opzionali)
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `has_docstring` | `Optional[bool]` | Se il modulo ha docstring |
| `num_classes` | `Optional[int]` | Numero di classi definite |
| `num_functions` | `Optional[int]` | Numero di funzioni/metodi |

### Proprietà Calcolate

```python
.filename           # Nome del file (es. "main.py")
.code_percentage    # % di codice sul totale
.comment_percentage # % di commenti sul totale
```

### Esempio

```python
stats = FileStats(
    path=Path("src/main.py"),
    total_lines=100,
    code_lines=70,
    comment_lines=20,
    blank_lines=10,
    language="Python",
    num_classes=2,
    num_functions=5
)

print(stats.filename)          # "main.py"
print(stats.code_percentage)   # 70.0
```

---

## 📁 DirectoryStats

**Rappresenta una directory con file e sottodirectory (struttura ad albero).**

### Attributi

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `path` | `Path` | Percorso della directory |
| `files` | `List[FileStats]` | File nella directory |
| `subdirectories` | `List[DirectoryStats]` | Sottodirectory (ricorsivo) |

### Proprietà Aggregate (Ricorsive)

Tutte le proprietà sommano i valori dalla directory corrente e da **tutte** le sottodirectory:

```python
.name                  # Nome della directory
.total_files           # Numero totale file
.total_lines           # Righe totali
.total_code_lines      # Righe di codice
.total_comment_lines   # Righe di commento
.total_blank_lines     # Righe vuote
.code_percentage       # % codice
.comment_percentage    # % commenti
.blank_percentage      # % righe vuote
```

### Metodi

#### `get_python_stats() -> dict`
Statistiche aggregate per file Python:
```python
{
    "num_classes": 15,           # Totale classi
    "num_functions": 42,         # Totale funzioni
    "files_with_docstring": 8,   # File con docstring
    "python_files": 10           # Numero file Python
}
```

#### `sort_files_by_size() -> None`
Ordina file per numero di righe (decrescente), ricorsivamente su tutte le subdirectory.

### Esempio

```python
# Struttura:
# project/
# ├── main.py (100 righe)
# └── utils/
#     └── helper.py (50 righe)

root = DirectoryStats(path=Path("project"))
root.files = [FileStats(...)]  # main.py
root.subdirectories = [utils_dir]

print(root.total_files)  # 2
print(root.total_lines)  # 150
print(root.name)         # "project"
```

---

## 🔄 Struttura Ricorsiva

`DirectoryStats` usa una struttura **ad albero**:

```
DirectoryStats (root)
├── files: [main.py, config.py]
└── subdirectories:
    ├── DirectoryStats (src/)
    │   ├── files: [core.py, utils.py]
    │   └── subdirectories: [...]
    └── DirectoryStats (tests/)
        ├── files: [test_main.py]
        └── subdirectories: []
```

Le proprietà aggregate attraversano tutto l'albero:
```python
root.total_lines = (
    sum(file.total_lines for file in root.files) +
    sum(subdir.total_lines for subdir in root.subdirectories)
)
```
---

## 📚 Riferimenti

- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Properties](https://docs.python.org/3/library/functions.html#property)
