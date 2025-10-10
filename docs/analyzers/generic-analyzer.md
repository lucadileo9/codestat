# 🌐 GenericAnalyzer - Analisi Multi-Linguaggio

**Pattern:** Strategy Pattern + Configuration-Driven  
**File:** `src/project_analyzer/analyzers/generic.py`

---

## 🎯 Scopo

Analizza file di **qualsiasi linguaggio** supportato usando pattern matching sulla sintassi dei commenti.  
Usa configurazione centralizzata per supportare 50+ linguaggi senza codice ripetitivo.

---

## 🏗️ Architettura

```
GenericAnalyzer
├── Usa: language_config.py (configurazione centralizzata)
├── Supporta: 50+ linguaggi
└── Metodo: Pattern matching su commenti
```

---

## 📋 Linguaggi Supportati

### **Stili di Commento**

| Stile | Linguaggi | Single-line | Multi-line |
|-------|-----------|-------------|------------|
| **C-style** | JavaScript, TypeScript, Java, C, C++, Go, Rust, Swift, Kotlin | `//` | `/* */` |
| **Hash** | Python, Ruby, Shell, Bash, Perl, R, YAML | `#` | - |
| **Dash** | SQL, Lua, Haskell | `--` | - |
| **Markup** | HTML, XML | - | `<!-- -->` |
| **CSS** | CSS, SCSS, Less | - | `/* */` |

### **Estensioni**

50+ estensioni supportate: `.js`, `.ts`, `.java`, `.cpp`, `.rs`, `.rb`, `.php`, `.go`, `.swift`, ecc.

---

## 🔧 Proprietà Principali

### **1. `supported_extensions`**

```python
@property
def supported_extensions(self) -> Set[str]:
    return set(LANGUAGE_MAP.keys())
```

**Ritorna:** Tutte le estensioni dalla configurazione centralizzata.

---

### **2. `language_name`**

```python
@property
def language_name(self) -> str:
    return "Generic"
```

---

## 🔍 Metodi Principali

### **1. `_get_language_for_file(file_path)` - Identifica Linguaggio**

```python
def _get_language_for_file(self, file_path: Path) -> str:
    ext = file_path.suffix.lower()  # ".js"
    return LANGUAGE_MAP.get(ext, "Unknown")  # "JavaScript"
```

**Esempio:**
```python
_get_language_for_file(Path("app.js"))      # "JavaScript"
_get_language_for_file(Path("script.py"))   # "Python"
```

---

### **2. `analyze(file_path)` - Analisi Completa**

**Flusso:**

```
1. Determina linguaggio dall'estensione
2. Conta righe base (totali, vuote)
3. Loop su ogni riga:
   ├─ Salta righe vuote
   ├─ Gestisci commenti multi-linea
   │  ├─ Già dentro? → Conta e cerca fine
   │  └─ Inizia nuovo? → Conta e controlla se finisce subito
   └─ Gestisci commenti singola linea
4. Calcola: code_lines = total - blank - comment
5. Ritorna FileStats
```

---

## 📝 Gestione Commenti

### **Commenti Singola Linea**

```python
if language_config.is_comment_start(stripped, language):
    comment_lines += 1
    continue
```

**Esempio:**
```javascript
// Questo è un commento  ← Rilevato
let x = 5;              ← Codice
```

---

### **Commenti Multi-Linea**

**State Machine:**
```
Stati:
- in_multiline_comment = False (modalità normale)
- in_multiline_comment = True (dentro commento)

Transizioni:
1. Trova inizio (/* o <!--) → Entra in modalità multi-linea
2. Trova fine (*/ o -->) → Esce dalla modalità
3. Se inizia e finisce sulla stessa riga → Non entra
```

---

## ⚙️ Configurazione (language_config.py)

### **LANGUAGE_MAP - Estensioni → Linguaggi**

```python
LANGUAGE_MAP = {
    '.js': 'JavaScript',
    '.py': 'Python',
    '.java': 'Java',
    # ... 50+ estensioni
}
```

---

### **COMMENT_SYNTAX - Sintassi Commenti**

```python
COMMENT_SYNTAX = {
    "c_style": {
        "languages": {'JavaScript', 'Java', 'C++', ...},
        "single_line": {CommentStyle.DOUBLE_SLASH},  # //
        "multi_line": {CommentStyle.C_MULTILINE}     # /* */
    },
    "hash_style": {
        "languages": {'Python', 'Ruby', ...},
        "single_line": {CommentStyle.HASH},          # #
        "multi_line": set()                          # Nessuno
    }
}
```

---

### **LanguageConfig - Helper Class**

**Metodi principali:**

```python
# Ottiene marker per commenti singola linea
markers = language_config.get_single_line_markers("JavaScript")
# {'//'}

# Verifica se riga inizia con commento
language_config.is_comment_start("// Comment", "JavaScript")
# True

# Trova inizio commento multi-linea
has_start, end = language_config.has_multiline_start("/* Start", "JavaScript")
# (True, '*/')

# Verifica fine commento multi-linea
language_config.has_multiline_end("End */", "*/")
# True
```

---
## 🚀 Vantaggi

### ✅ **1. Estendibilità**
```python
# Aggiungi Zig in 2 righe!
LANGUAGE_MAP['.zig'] = 'Zig'
COMMENT_SYNTAX["c_style"]["languages"].add('Zig')
# Fatto! Funziona subito
```

### ✅ **2. Manutenibilità**
- Configurazione separata dalla logica
- Nessun if ripetitivo
- Facile da testare

### ✅ **3. Performance**
- Lookup in Set: O(1)
- Parsing lineare: O(n) righe
- Nessuna regex complessa

### ✅ **4. Supporto Multi-Linguaggio**
- 50+ linguaggi con un solo analyzer
- Configurazione dichiarativa
- Comportamento uniforme

---

## ⚠️ Limitazioni

### ❌ **1. Commenti Inline**
```javascript
let x = 5;  // Commento inline  ← Contato come CODICE
```

**Perché:** La riga non **inizia** con `//`, quindi non è rilevata.

---

### ❌ **2. # in Stringhe**
```python
url = "http://example.com"  # ← // non è commento (giusto!)
# Ma con pattern semplice potrebbe confondersi
```

**Soluzione:** Il tokenizer di PythonAnalyzer gestisce questo meglio.

---

### ❌ **3. Codice Commentato**
```javascript
// let x = 5;  ← È codice o commento?
```

**Impossibile distinguere** senza eseguire analisi semantica avanzata.

---
## 📚 Riferimenti

- `language_config.py` - Configurazione centralizzata
- `base.py` - Interfaccia comune
- [Documentazione Models](../models.md)
