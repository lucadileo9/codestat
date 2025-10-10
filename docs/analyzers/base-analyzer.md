# 🎨 BaseAnalyzer - Interfaccia Comune

**Pattern:** Strategy Pattern  
**File:** `src/project_analyzer/analyzers/base.py`

---

## 🎯 Scopo

Definisce l'**interfaccia comune** che tutti gli analyzer devono implementare.  
Fornisce metodi helper condivisi per evitare duplicazione di codice.

---

## 📐 Classe Astratta

```python
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """Classe base per tutti gli analyzer."""
```

**Cos'è ABC?**
- **Abstract Base Class**: classe che non può essere istanziata direttamente
- Forza le sottoclassi a implementare metodi specifici
- Garantisce un'interfaccia uniforme

---

## 🔧 Metodi Astratti (da Implementare)

### **1. `supported_extensions` (proprietà)**

```python
@property
@abstractmethod
def supported_extensions(self) -> Set[str]:
    """Estensioni file supportate dall'analyzer."""
    pass
```

**Deve ritornare:** Set di estensioni (es. `{'.py', '.pyw'}`)

**Esempio implementazione:**
```python
@property
def supported_extensions(self) -> Set[str]:
    return {'.js', '.ts', '.jsx', '.tsx'}
```

---

### **2. `language_name` (proprietà)**

```python
@property
@abstractmethod
def language_name(self) -> str:
    """Nome del linguaggio/analyzer."""
    pass
```

**Deve ritornare:** Nome come stringa (es. `"Python"`, `"JavaScript"`, `"Generic"`)

---

### **3. `analyze(file_path)` (metodo)**

```python
@abstractmethod
def analyze(self, file_path: Path) -> FileStats:
    """
    Analizza un file e ritorna le statistiche.
    
    Args:
        file_path: Path del file da analizzare
        
    Returns:
        FileStats con le statistiche complete
    """
    pass
```

**Responsabilità:**
- Leggere il file
- Contare righe (totali, codice, commenti, vuote)
- Ritornare un oggetto `FileStats`

---

## 🛠️ Metodi Helper (già Implementati)

### **1. `can_analyze(file_path)` - Verifica Supporto**

```python
def can_analyze(self, file_path: Path) -> bool:
    """Verifica se l'analyzer può gestire il file."""
    return file_path.suffix.lower() in self.supported_extensions
```

**Uso:**
```python
analyzer = PythonAnalyzer()
analyzer.can_analyze(Path("script.py"))   # True
analyzer.can_analyze(Path("app.js"))      # False
```

---

### **2. `_count_lines(file_path)` - Conteggio Base**

```python
def _count_lines(self, file_path: Path) -> tuple[int, int, list[str]]:
    """
    Conta righe totali e vuote, ritorna anche le righe.
    
    Returns:
        (total_lines, blank_lines, lines)
    """
```

**Cosa fa:**
1. Legge il file con encoding UTF-8
2. Conta righe totali
3. Conta righe vuote (solo spazi/tab)
4. Ritorna tutto insieme

**Esempio:**
```python
total, blank, lines = self._count_lines(Path("example.py"))
# total = 100
# blank = 15
# lines = ['import os\n', '\n', 'def main():\n', ...]
```

**Gestione errori:**
```python
try:
    # Legge file
except UnicodeDecodeError:
    return 0, 0, []  # File non leggibile
except Exception:
    return 0, 0, []  # Altri errori
```

---

## 🎯 Come Creare un Nuovo Analyzer

Vedi gli esempi dell'analyzer Python e Generic per ispirazione.

---
## 🔑 Concetti Chiave

| Concetto | Spiegazione |
|----------|-------------|
| **ABC** | Classe astratta, non istanziabile |
| **@abstractmethod** | Metodo che DEVE essere implementato |
| **@property** | Metodo usato come attributo |
| **Strategy Pattern** | Intercambiabilità degli algoritmi |
| **Helper methods** | Metodi comuni condivisi (`_count_lines`) |

---

## 📚 Riferimenti

- [ABC - Python Docs](https://docs.python.org/3/library/abc.html)
- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
