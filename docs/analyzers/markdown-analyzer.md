# MarkdownAnalyzer

Questo documento descrive il `MarkdownAnalyzer`, l'analyzer dedicato ai file di documentazione in formato Markdown (.md).

## Scopo

`MarkdownAnalyzer` fornisce metriche utili sui file Markdown, pensate per valutare la struttura e la presenza di elementi tipici della documentazione (titoli, link, immagini, blocchi di codice, tabelle). È progettato per essere leggero e senza dipendenze esterne: usa semplici euristiche testuali per estrarre le informazioni.

## Quando usarlo

- Vuoi includere i file `.md` nella codebase analysis
- Ti interessa il numero e la profondità dei titoli (per valutare la struttura dei contenuti)
- Vuoi contare link, immagini, blocchi di codice e presenza di tabelle

## Metriche calcolate

Per ogni file Markdown l'analyzer restituisce un `FileStats` (come per gli altri analyzer) e allega dinamicamente un dizionario `markdown_stats` con i seguenti campi:

- `headings_by_level`: dict {1..6} -> conteggio titoli per livello (es. h1, h2, ...)
- `num_headings`: numero totale di titoli
- `num_links`: conteggio di occorrenze del pattern `[text](url)` (esclusi gli elementi immagine)
- `num_images`: conteggio di occorrenze del pattern `![alt](url)`
- `num_code_blocks`: numero di blocchi di codice fenced (delimitati da ```)
- `num_tables`: conteggio (euristico) di tabelle Markdown con riga divider

Nota: `FileStats` contiene le proprietà base (total_lines, code_lines, blank_lines). I metadati Markdown sono aggiunti dinamicamente a `file_stats.markdown_stats` per evitare di cambiare il modello dati centrale.

## Come funziona (breve)

- Legge il file linea per linea usando l'helper di `BaseAnalyzer` per supportare diversi encoding.
- Ignora il contenuto interno ai blocchi di codice fenced quando rileva headings/links.
- Usa espressioni regolari semplici per identificare heading, link, immagini e la riga divider delle tabelle.

Queste euristiche sono deliberate: sono rapide e non richiedono librerie aggiuntive. Per esigenze più sofisticate è possibile integrare un parser Markdown (vedi "Possibili miglioramenti").

## Esempio di output (ConsoleReporter)

Durante il report console, per un file `README.md` potresti vedere:

📄 README.md
│     Lines: 199 | Code: 160 | Comments: 0 | Blank: 39
│     📝 Markdown: 18 headings, 2 links, 0 images
│     🧾 Code blocks: 2 | Tables: 0
│     🔢 Headings by level: h1:1, h2:8, h3:6, h4:3

I dati provengono da `file_stats.markdown_stats`.

## Estensioni supportate

- `.md`
- `.markdown`

Il `MarkdownAnalyzer` è registrato insieme agli altri analyzer all'interno di `ProjectAnalyzer`, quindi i file `.md` vengono analizzati automaticamente (se non si usano filtri di estensione espliciti).

## Come eseguire

Dal folder `src` (metodo rapido senza installazione):

```powershell
cd C:\Users\<you>\my-projects\codestat\src
python -m project_analyzer C:\percorso\al\progetto
```

Oppure installa il package in editable e poi esegui da qualsiasi posizione:

```powershell
pip install -e .
python -m project_analyzer C:\percorso\al\progetto
```

---

Per dettagli sul modello `FileStats` e su come vengono aggregate le statistiche di directory, vedi `docs/models.md` e la documentazione del `core`.
