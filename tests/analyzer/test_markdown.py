import pytest
from project_analyzer.analyzers.markdown import MarkdownAnalyzer
from pathlib import Path


class TestMarkdownAnalyzer:

    def setup_method(self):
        """Inizializza l'istanza dell'analizzatore prima di ciascun test."""
        self.analyzer = MarkdownAnalyzer()

    def teardown_method(self):
        """Pulisce l'istanza dell'analizzatore dopo ciascun test."""
        del self.analyzer

    def test_supported_extensions_is_set(self):
        """Verifica che supported_extensions sia un set."""
        assert isinstance(self.analyzer.supported_extensions, set)

    def test_supported_extensions_contains_expected_items(self):
        """Controlla che le estensioni comuni di Markdown siano presenti."""
        assert self.analyzer.supported_extensions == {".md", ".markdown"}

    def test_can_analyze_md_extension(self):
        """Verifica che un file con estensione .md venga riconosciuto come analizzabile."""
        assert self.analyzer.can_analyze(Path("README.md"))

    def test_can_analyze_md_extension_case_insensitive(self):
        """Verifica che il riconoscimento dell'estensione sia case-insensitive."""
        assert self.analyzer.can_analyze(Path("README.MD"))

    def test_can_analyze_markdown_extension(self):
        """Verifica che l'estensione .markdown venga riconosciuta come valida."""
        assert self.analyzer.can_analyze(Path("notes.markdown"))

    def test_cannot_analyze_unsupported_extension(self):
        """Verifica che estensioni non previste non siano considerate analizzabili."""
        assert not self.analyzer.can_analyze(Path("document.txt"))

    def test_language_name_property_returns_markdown(self):
        """Controlla che la proprietà language_name ritorni 'Markdown'."""
        assert self.analyzer.language_name == "Markdown"

    def test_language_name_is_str_and_consistent_across_instances(self):
        """Verifica che il nome del linguaggio sia stringa e coerente tra istanze."""
        a1 = self.analyzer
        a2 = MarkdownAnalyzer()
        assert isinstance(a1.language_name, str)
        assert a1.language_name == a2.language_name == "Markdown"

    def test_analyze_counts_headings_links_images_codeblocks_tables_and_blank_lines(
        self, tmp_path: Path
    ):
        """Esegue l'analisi di un file di esempio e verifica conteggi tipici del Markdown."""
        content = (
            "# Heading 1\n"
            "\n"
            "## Heading 2\n"
            "Regular paragraph with a [link](http://example.com) and an image ![alt](img.png)\n"
            "Another link [other](x)\n"
            "```\n"
            "## Not a heading inside code\n"
            "```\n"
            "```python\n"
            "Some code with [link](x) and ![img](y)\n"
            "```\n"
            "Table header | Column\n"
            "| --- | --- |\n"
            "\n"
            "End\n"
        )

        file_path = tmp_path / "sample.md"
        file_path.write_text(content, encoding="utf-8")

        fs = self.analyzer.analyze(file_path)

        # Basic file stats
        assert fs.path == file_path
        assert fs.total_lines == 15
        assert fs.blank_lines == 2
        assert fs.code_lines == 13
        assert fs.comment_lines == 0
        assert fs.language == "Markdown"

        md = fs.markdown_stats
        # Headings: one H1 and one H2; heading inside fenced code ignored
        assert md["num_headings"] == 2
        assert md["headings_by_level"][1] == 1
        assert md["headings_by_level"][2] == 1
        # No other heading levels present
        for lvl in (3, 4, 5, 6):
            assert md["headings_by_level"][lvl] == 0

        # Links and images: two links (one in same line as image), one image; links/images inside code fences ignored
        assert md["num_links"] == 2
        assert md["num_images"] == 1

        # Two fenced code blocks opened (``` and ```python)
        assert md["num_code_blocks"] == 2

        # One table detected by header + divider heuristic
        assert md["num_tables"] == 1
