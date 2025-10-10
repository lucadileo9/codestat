from pathlib import Path
import re
from .base import BaseAnalyzer
from ..models import FileStats
from typing import Set, Dict, List


class MarkdownAnalyzer(BaseAnalyzer):
    """
    Analyzer per file Markdown (.md).
    Analizza titoli (per livello), link, immagini, blocchi di codice fenced e tabelle.
    I metadati specifici Markdown vengono allegati dinamicamente al FileStats
    nel campo `markdown_stats` (dict) per evitare modifiche a `models.py`.
    """

    @property
    def supported_extensions(self) -> Set[str]:
        """Estensioni Markdown supportate."""
        return {'.md', '.markdown'}

    @property
    def language_name(self) -> str:
        """Nome del linguaggio."""
        return "Markdown"

    def can_analyze(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.supported_extensions

    def analyze(self, file_path: Path) -> FileStats:
        """
        Analyzes a Markdown file to extract statistics such as line counts, headings, links, images, code blocks, and tables.
        Args:
            file_path (Path): The path to the Markdown file to analyze.
        Returns:
            FileStats: An object containing statistics about the file, including:
                - total_lines: Total number of lines in the file.
                - code_lines: Number of non-blank lines.
                - comment_lines: Always 0 for Markdown.
                - blank_lines: Number of blank lines.
                - language: Set to "Markdown".
                - markdown_stats (dict): Additional Markdown-specific statistics:
                    - 'headings_by_level': Dict mapping heading levels (1-6) to their counts.
                    - 'num_headings': Total number of headings.
                    - 'num_links': Number of Markdown links (excluding images).
                    - 'num_images': Number of images.
                    - 'num_code_blocks': Number of fenced code blocks.
                    - 'num_tables': Number of tables (heuristically detected).
        """
        # Usa l'helper del BaseAnalyzer per ottenere lines in modo robusto
        total_lines, blank_lines, lines = self._count_lines(file_path)

        headings_by_level: Dict[int, int] = {i: 0 for i in range(1, 7)}
        heading_lines = 0
        link_count = 0
        image_count = 0
        code_block_count = 0
        table_count = 0

        in_fenced_code = False

        # Compila regex utili
        re_heading = re.compile(r'^\s*(#{1,6})\s+')
        re_image = re.compile(r'!\[[^\]]*\]\([^\)]+\)')
        re_link = re.compile(r'(?<!\!)\[[^\]]+\]\([^\)]+\)')
        # Allow optional trailing pipe so patterns like '| --- | --- |' match
        re_table_divider = re.compile(r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$')

        for i, raw in enumerate(lines):
            line = raw.rstrip('\n')
            stripped = line.strip()

            # Gestione blocchi di codice fenced (```)
            if stripped.startswith('```'):
                # Toggle stato e conta l'apertura del blocco
                if not in_fenced_code:
                    code_block_count += 1
                    in_fenced_code = True
                else:
                    in_fenced_code = False
                # continua, non considerare il contenuto del fence per headings/links
                continue

            if in_fenced_code:
                # Ignora contenuto interno ai blocchi di codice
                continue

            # Headings
            m = re_heading.match(line)
            if m:
                level = len(m.group(1))
                headings_by_level[level] += 1
                heading_lines += 1

            # Images
            if re_image.search(line):
                image_count += len(re_image.findall(line))

            # Links (esclusi quelli che erano immagini)
            if re_link.search(line):
                link_count += len(re_link.findall(line))

            # Tables: semplice euristica - se la linea contiene '|' e la successiva è una divider
            if '|' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if re_table_divider.match(next_line):
                    table_count += 1

        # Costruisci FileStats
        fs = FileStats(
            path=file_path,
            total_lines=total_lines,
            code_lines=max(0, total_lines - blank_lines),
            comment_lines=0,
            blank_lines=blank_lines,
            language="Markdown",
        )

        # Allego metadati Markdown dinamicamente per non toccare models.py
        fs.markdown_stats = {
            'headings_by_level': headings_by_level,
            'num_headings': heading_lines,
            'num_links': link_count,
            'num_images': image_count,
            'num_code_blocks': code_block_count,
            'num_tables': table_count,
        }

        return fs
