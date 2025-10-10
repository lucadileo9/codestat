"""
Test per models.py - FileStats e DirectoryStats.
"""

import pytest
from pathlib import Path
from src.project_analyzer.models import FileStats, DirectoryStats


# ============================================================================
# TEST FILESTATS - FILENAME PROPERTY
# ============================================================================


class TestFileStatsFilename:
    """Test suite for FileStats.filename property."""

    def test_filename_simple_file(self):
        """Test filename property returns correct name for simple file."""
        file_stats = FileStats(path=Path("test.py"))
        assert file_stats.filename == "test.py"

    def test_filename_with_path(self):
        """Test filename property returns only filename from full path."""
        file_stats = FileStats(path=Path("/home/user/project/module.py"))
        assert file_stats.filename == "module.py"

    def test_filename_windows_path(self):
        """Test filename property with Windows-style path."""
        file_stats = FileStats(path=Path("C:/Users/lucad/my-projects/codestat/src/main.py"))
        assert file_stats.filename == "main.py"

    def test_filename_nested_directories(self):
        """Test filename property with deeply nested directories."""
        file_stats = FileStats(path=Path("a/b/c/d/e/file.txt"))
        assert file_stats.filename == "file.txt"

    def test_filename_with_multiple_extensions(self):
        """Test filename property with multiple extensions."""
        file_stats = FileStats(path=Path("archive.tar.gz"))
        assert file_stats.filename == "archive.tar.gz"

    def test_filename_no_extension(self):
        """Test filename property for file without extension."""
        file_stats = FileStats(path=Path("/usr/bin/python"))
        assert file_stats.filename == "python"

    def test_filename_hidden_file(self):
        """Test filename property for hidden file (Unix-style)."""
        file_stats = FileStats(path=Path(".gitignore"))
        assert file_stats.filename == ".gitignore"


# ============================================================================
# TEST FILESTATS - CODE_PERCENTAGE PROPERTY
# ============================================================================


class TestFileStatsCodePercentage:
    """Test suite for FileStats.code_percentage property."""

    def test_code_percentage_zero_lines(self):
        """Test code_percentage returns 0.0 when total_lines is 0."""
        file_stats = FileStats(path=Path("empty.py"), total_lines=0, code_lines=0)
        assert file_stats.code_percentage == 0.0

    def test_code_percentage_all_code_lines(self):
        """Test code_percentage returns 100% when all lines are code."""
        file_stats = FileStats(path=Path("test.py"), total_lines=100, code_lines=100)
        assert file_stats.code_percentage == 100.0

    def test_code_percentage_half_code_lines(self):
        """Test code_percentage returns 50% when half lines are code."""
        file_stats = FileStats(path=Path("test.py"), total_lines=100, code_lines=50)
        assert file_stats.code_percentage == 50.0

    def test_code_percentage_no_code_lines(self):
        """Test code_percentage returns 0% when no code lines exist."""
        file_stats = FileStats(path=Path("test.py"), total_lines=100, code_lines=0)
        assert file_stats.code_percentage == 0.0

    def test_code_percentage_fractional_result(self):
        """Test code_percentage calculates fractional percentages correctly."""
        file_stats = FileStats(path=Path("test.py"), total_lines=3, code_lines=1)
        assert file_stats.code_percentage == pytest.approx(33.333333, rel=1e-5)

    def test_code_percentage_one_line_file(self):
        """Test code_percentage for single line file."""
        file_stats = FileStats(path=Path("test.py"), total_lines=1, code_lines=1)
        assert file_stats.code_percentage == 100.0

    def test_code_percentage_realistic_file(self):
        """Test code_percentage with realistic file statistics."""
        file_stats = FileStats(
            path=Path("module.py"),
            total_lines=200,
            code_lines=120,
            comment_lines=50,
            blank_lines=30,
        )
        assert file_stats.code_percentage == 60.0

    def test_code_percentage_small_ratio(self):
        """Test code_percentage with very small code ratio."""
        file_stats = FileStats(path=Path("test.py"), total_lines=1000, code_lines=1)
        assert file_stats.code_percentage == 0.1


# ============================================================================
# TEST FILESTATS - COMMENT_PERCENTAGE PROPERTY
# ============================================================================


class TestFileStatsCommentPercentage:
    """Test suite for FileStats.comment_percentage property."""

    def test_comment_percentage_zero_lines(self):
        """Test comment_percentage returns 0.0 when total_lines is 0."""
        file_stats = FileStats(path=Path("empty.py"), total_lines=0, comment_lines=0)
        assert file_stats.comment_percentage == 0.0

    def test_comment_percentage_all_comment_lines(self):
        """Test comment_percentage returns 100% when all lines are comments."""
        file_stats = FileStats(path=Path("test.py"), total_lines=100, comment_lines=100)
        assert file_stats.comment_percentage == 100.0

    def test_comment_percentage_half_comment_lines(self):
        """Test comment_percentage returns 50% when half lines are comments."""
        file_stats = FileStats(path=Path("test.py"), total_lines=100, comment_lines=50)
        assert file_stats.comment_percentage == 50.0

    def test_comment_percentage_no_comment_lines(self):
        """Test comment_percentage returns 0% when no comment lines exist."""
        file_stats = FileStats(path=Path("test.py"), total_lines=100, comment_lines=0)
        assert file_stats.comment_percentage == 0.0

    def test_comment_percentage_fractional_result(self):
        """Test comment_percentage calculates fractional percentages correctly."""
        file_stats = FileStats(path=Path("test.py"), total_lines=3, comment_lines=1)
        assert file_stats.comment_percentage == pytest.approx(33.333333, rel=1e-5)

    def test_comment_percentage_one_line_file(self):
        """Test comment_percentage for single line file with comment."""
        file_stats = FileStats(path=Path("test.py"), total_lines=1, comment_lines=1)
        assert file_stats.comment_percentage == 100.0

    def test_comment_percentage_realistic_file(self):
        """Test comment_percentage with realistic file statistics."""
        file_stats = FileStats(
            path=Path("module.py"),
            total_lines=200,
            code_lines=120,
            comment_lines=50,
            blank_lines=30,
        )
        assert file_stats.comment_percentage == 25.0

    def test_comment_percentage_small_ratio(self):
        """Test comment_percentage with very small comment ratio."""
        file_stats = FileStats(path=Path("test.py"), total_lines=1000, comment_lines=1)
        assert file_stats.comment_percentage == 0.1

    def test_comment_percentage_well_documented_file(self):
        """Test comment_percentage for well-documented file."""
        file_stats = FileStats(
            path=Path("documented.py"),
            total_lines=100,
            code_lines=40,
            comment_lines=40,
            blank_lines=20,
        )
        assert file_stats.comment_percentage == 40.0


# ============================================================================
# TEST FILESTATS - __STR__ METHOD
# ============================================================================


class TestFileStatsStr:
    """Test suite for FileStats.__str__ method."""

    def test_str_basic_file(self):
        """Test __str__ returns correctly formatted string for basic file."""
        file_stats = FileStats(
            path=Path("test.py"), total_lines=100, code_lines=70, comment_lines=20, blank_lines=10
        )
        expected = "test.py: 100 lines (70 code, 20 comments, 10 blank)"
        assert str(file_stats) == expected

    def test_str_empty_file(self):
        """Test __str__ with empty file (all zeros)."""
        file_stats = FileStats(path=Path("empty.py"))
        expected = "empty.py: 0 lines (0 code, 0 comments, 0 blank)"
        assert str(file_stats) == expected

    def test_str_only_code_lines(self):
        """Test __str__ when file has only code lines."""
        file_stats = FileStats(
            path=Path("code.py"), total_lines=50, code_lines=50, comment_lines=0, blank_lines=0
        )
        expected = "code.py: 50 lines (50 code, 0 comments, 0 blank)"
        assert str(file_stats) == expected

    def test_str_only_comments(self):
        """Test __str__ when file has only comment lines."""
        file_stats = FileStats(
            path=Path("comments.py"), total_lines=30, code_lines=0, comment_lines=30, blank_lines=0
        )
        expected = "comments.py: 30 lines (0 code, 30 comments, 0 blank)"
        assert str(file_stats) == expected

    def test_str_only_blank_lines(self):
        """Test __str__ when file has only blank lines."""
        file_stats = FileStats(
            path=Path("blank.py"), total_lines=15, code_lines=0, comment_lines=0, blank_lines=15
        )
        expected = "blank.py: 15 lines (0 code, 0 comments, 15 blank)"
        assert str(file_stats) == expected

    def test_str_single_line_file(self):
        """Test __str__ with single line file."""
        file_stats = FileStats(
            path=Path("single.py"), total_lines=1, code_lines=1, comment_lines=0, blank_lines=0
        )
        expected = "single.py: 1 lines (1 code, 0 comments, 0 blank)"
        assert str(file_stats) == expected

    def test_str_with_full_path(self):
        """Test __str__ uses only filename, not full path."""
        file_stats = FileStats(
            path=Path("/home/user/project/src/module.py"),
            total_lines=200,
            code_lines=150,
            comment_lines=30,
            blank_lines=20,
        )
        expected = "module.py: 200 lines (150 code, 30 comments, 20 blank)"
        assert str(file_stats) == expected

    def test_str_large_file(self):
        """Test __str__ with large file statistics."""
        file_stats = FileStats(
            path=Path("large.py"),
            total_lines=10000,
            code_lines=7500,
            comment_lines=1500,
            blank_lines=1000,
        )
        expected = "large.py: 10000 lines (7500 code, 1500 comments, 1000 blank)"
        assert str(file_stats) == expected

    def test_str_file_with_extension(self):
        """Test __str__ with various file extensions."""
        file_stats = FileStats(
            path=Path("script.js"), total_lines=80, code_lines=60, comment_lines=15, blank_lines=5
        )
        expected = "script.js: 80 lines (60 code, 15 comments, 5 blank)"
        assert str(file_stats) == expected

    def test_str_realistic_python_file(self):
        """Test __str__ with realistic Python file statistics."""
        file_stats = FileStats(
            path=Path("models.py"),
            total_lines=500,
            code_lines=320,
            comment_lines=100,
            blank_lines=80,
            language="Python",
        )
        expected = "models.py: 500 lines (320 code, 100 comments, 80 blank)"
        assert str(file_stats) == expected
        # ============================================================================
        # TEST DIRECTORYSTATS - NAME PROPERTY
        # ============================================================================


class TestDirectoryStatsName:
    """Test suite for DirectoryStats.name property."""

    def test_name_simple_directory(self):
        """Test name property returns correct name for simple directory."""
        dir_stats = DirectoryStats(path=Path("src"))
        assert dir_stats.name == "src"

    def test_name_with_path(self):
        """Test name property returns only directory name from full path."""
        dir_stats = DirectoryStats(path=Path("/home/user/project/src"))
        assert dir_stats.name == "src"

    def test_name_windows_path(self):
        """Test name property with Windows-style path."""
        dir_stats = DirectoryStats(path=Path("C:/Users/lucad/my-projects/codestat"))
        assert dir_stats.name == "codestat"

    def test_name_nested_directories(self):
        """Test name property with deeply nested directories."""
        dir_stats = DirectoryStats(path=Path("a/b/c/d/e"))
        assert dir_stats.name == "e"

    def test_name_current_directory(self):
        """Test name property for current directory."""
        dir_stats = DirectoryStats(path=Path("."))
        assert dir_stats.name == "."

    def test_name_parent_directory(self):
        """Test name property for parent directory."""
        dir_stats = DirectoryStats(path=Path(".."))
        assert dir_stats.name == ".."

    def test_name_hidden_directory(self):
        """Test name property for hidden directory (Unix-style)."""
        dir_stats = DirectoryStats(path=Path(".git"))
        assert dir_stats.name == ".git"

    def test_name_directory_with_spaces(self):
        """Test name property for directory with spaces in name."""
        dir_stats = DirectoryStats(path=Path("my project"))
        assert dir_stats.name == "my project"

    def test_name_directory_with_special_chars(self):
        """Test name property for directory with special characters."""
        dir_stats = DirectoryStats(path=Path("project-2024_v1"))
        assert dir_stats.name == "project-2024_v1"

    def test_name_empty_path_fallback(self):
        """Test name property fallback when path.name is empty."""
        dir_stats = DirectoryStats(path=Path(""))
        # When path.name is empty, should return str(path)
        assert dir_stats.name == "."
        # ============================================================================
        # TEST DIRECTORYSTATS - TOTAL_FILES PROPERTY
        # ============================================================================


class TestDirectoryStatsTotalFiles:
    """Test suite for DirectoryStats.total_files property."""

    def test_total_files_empty_directory(self):
        """Test total_files returns 0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.total_files == 0

    def test_total_files_single_file(self):
        """Test total_files returns 1 for directory with single file."""
        dir_stats = DirectoryStats(path=Path("src"), files=[FileStats(path=Path("src/main.py"))])
        assert dir_stats.total_files == 1

    def test_total_files_multiple_files(self):
        """Test total_files returns correct count for multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(path=Path("src/main.py")),
                FileStats(path=Path("src/utils.py")),
                FileStats(path=Path("src/config.py")),
            ],
        )
        assert dir_stats.total_files == 3

    def test_total_files_with_single_subdirectory(self):
        """Test total_files counts files in subdirectories."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(path=Path("src/helpers/util1.py")),
                FileStats(path=Path("src/helpers/util2.py")),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"))],
            subdirectories=[subdir],
        )
        assert dir_stats.total_files == 3

    def test_total_files_with_multiple_subdirectories(self):
        """Test total_files counts files across multiple subdirectories."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[FileStats(path=Path("src/models/user.py"))],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(path=Path("src/views/home.py")),
                FileStats(path=Path("src/views/about.py")),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"))],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_files == 4

    def test_total_files_nested_subdirectories(self):
        """Test total_files recursively counts files in nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[FileStats(path=Path("src/utils/helpers/helper.py"))],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[FileStats(path=Path("src/utils/util.py"))],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"))],
            subdirectories=[mid_subdir],
        )
        assert dir_stats.total_files == 3

    def test_total_files_only_subdirectories(self):
        """Test total_files when directory has no direct files."""
        subdir = DirectoryStats(
            path=Path("src/lib"),
            files=[
                FileStats(path=Path("src/lib/lib1.py")),
                FileStats(path=Path("src/lib/lib2.py")),
            ],
        )
        dir_stats = DirectoryStats(path=Path("src"), files=[], subdirectories=[subdir])
        assert dir_stats.total_files == 2

    def test_total_files_complex_structure(self):
        """Test total_files with complex directory structure."""
        subdir1_1 = DirectoryStats(
            path=Path("src/models/entities"),
            files=[FileStats(path=Path("src/models/entities/user.py"))],
        )
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[FileStats(path=Path("src/models/base.py"))],
            subdirectories=[subdir1_1],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(path=Path("src/views/home.py")),
                FileStats(path=Path("src/views/about.py")),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(path=Path("src/main.py")),
                FileStats(path=Path("src/config.py")),
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_files == 6

    def test_total_files_empty_subdirectories(self):
        """Test total_files with empty subdirectories."""
        subdir1 = DirectoryStats(path=Path("src/empty1"))
        subdir2 = DirectoryStats(path=Path("src/empty2"))
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"))],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_files == 1

    def test_total_files_large_number_of_files(self):
        """Test total_files with large number of files."""
        files = [FileStats(path=Path(f"src/file{i}.py")) for i in range(100)]
        dir_stats = DirectoryStats(path=Path("src"), files=files)
        assert dir_stats.total_files == 100

    def test_total_files_deeply_nested_structure(self):
        """Test total_files with deeply nested directory structure."""
        level3 = DirectoryStats(
            path=Path("src/a/b/c"),
            files=[FileStats(path=Path("src/a/b/c/file.py"))],
        )
        level2 = DirectoryStats(
            path=Path("src/a/b"),
            files=[FileStats(path=Path("src/a/b/file.py"))],
            subdirectories=[level3],
        )
        level1 = DirectoryStats(
            path=Path("src/a"),
            files=[FileStats(path=Path("src/a/file.py"))],
            subdirectories=[level2],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/file.py"))],
            subdirectories=[level1],
        )
        assert dir_stats.total_files == 4
        # ============================================================================
        # TEST DIRECTORYSTATS - TOTAL_LINES PROPERTY
        # ============================================================================


class TestDirectoryStatsTotalLines:
    """Test suite for DirectoryStats.total_lines property."""

    def test_total_lines_empty_directory(self):
        """Test total_lines returns 0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.total_lines == 0

    def test_total_lines_single_file(self):
        """Test total_lines returns correct count for single file."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"), total_lines=100)],
        )
        assert dir_stats.total_lines == 100

    def test_total_lines_multiple_files(self):
        """Test total_lines sums lines from multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(path=Path("src/main.py"), total_lines=100),
                FileStats(path=Path("src/utils.py"), total_lines=50),
                FileStats(path=Path("src/config.py"), total_lines=25),
            ],
        )
        assert dir_stats.total_lines == 175

    def test_total_lines_with_single_subdirectory(self):
        """Test total_lines includes lines from subdirectories."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(path=Path("src/helpers/util1.py"), total_lines=30),
                FileStats(path=Path("src/helpers/util2.py"), total_lines=40),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"), total_lines=100)],
            subdirectories=[subdir],
        )
        assert dir_stats.total_lines == 170

    def test_total_lines_with_multiple_subdirectories(self):
        """Test total_lines sums lines across multiple subdirectories."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[FileStats(path=Path("src/models/user.py"), total_lines=80)],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(path=Path("src/views/home.py"), total_lines=60),
                FileStats(path=Path("src/views/about.py"), total_lines=40),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"), total_lines=100)],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_lines == 280

    def test_total_lines_nested_subdirectories(self):
        """Test total_lines recursively counts lines in nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[FileStats(path=Path("src/utils/helpers/helper.py"), total_lines=20)],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[FileStats(path=Path("src/utils/util.py"), total_lines=50)],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"), total_lines=100)],
            subdirectories=[mid_subdir],
        )
        assert dir_stats.total_lines == 170

    def test_total_lines_only_subdirectories(self):
        """Test total_lines when directory has no direct files."""
        subdir = DirectoryStats(
            path=Path("src/lib"),
            files=[
                FileStats(path=Path("src/lib/lib1.py"), total_lines=75),
                FileStats(path=Path("src/lib/lib2.py"), total_lines=125),
            ],
        )
        dir_stats = DirectoryStats(path=Path("src"), files=[], subdirectories=[subdir])
        assert dir_stats.total_lines == 200

    def test_total_lines_complex_structure(self):
        """Test total_lines with complex directory structure."""
        subdir1_1 = DirectoryStats(
            path=Path("src/models/entities"),
            files=[
                FileStats(
                    path=Path("src/models/entities/user.py"),
                    total_lines=150,
                )
            ],
        )
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[FileStats(path=Path("src/models/base.py"), total_lines=200)],
            subdirectories=[subdir1_1],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(path=Path("src/views/home.py"), total_lines=100),
                FileStats(path=Path("src/views/about.py"), total_lines=80),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(path=Path("src/main.py"), total_lines=250),
                FileStats(path=Path("src/config.py"), total_lines=50),
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_lines == 830

    def test_total_lines_empty_subdirectories(self):
        """Test total_lines with empty subdirectories."""
        subdir1 = DirectoryStats(path=Path("src/empty1"))
        subdir2 = DirectoryStats(path=Path("src/empty2"))
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/main.py"), total_lines=100)],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_lines == 100

    def test_total_lines_files_with_zero_lines(self):
        """Test total_lines with files containing zero lines."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(path=Path("src/empty1.py"), total_lines=0),
                FileStats(path=Path("src/empty2.py"), total_lines=0),
                FileStats(path=Path("src/main.py"), total_lines=100),
            ],
        )
        assert dir_stats.total_lines == 100

    def test_total_lines_deeply_nested_structure(self):
        """Test total_lines with deeply nested directory structure."""
        level3 = DirectoryStats(
            path=Path("src/a/b/c"),
            files=[FileStats(path=Path("src/a/b/c/file.py"), total_lines=25)],
        )
        level2 = DirectoryStats(
            path=Path("src/a/b"),
            files=[FileStats(path=Path("src/a/b/file.py"), total_lines=50)],
            subdirectories=[level3],
        )
        level1 = DirectoryStats(
            path=Path("src/a"),
            files=[FileStats(path=Path("src/a/file.py"), total_lines=75)],
            subdirectories=[level2],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[FileStats(path=Path("src/file.py"), total_lines=100)],
            subdirectories=[level1],
        )
        assert dir_stats.total_lines == 250

    def test_total_lines_large_numbers(self):
        """Test total_lines with large line counts."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(path=Path("src/large1.py"), total_lines=10000),
                FileStats(path=Path("src/large2.py"), total_lines=15000),
                FileStats(path=Path("src/large3.py"), total_lines=20000),
            ],
        )
        assert dir_stats.total_lines == 45000
        # ============================================================================
        # TEST DIRECTORYSTATS - TOTAL_CODE_LINES PROPERTY
        # ============================================================================


class TestDirectoryStatsTotalCodeLines:
    """Test suite for DirectoryStats.total_code_lines property."""

    def test_total_code_lines_empty_directory(self):
        """Test total_code_lines returns 0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.total_code_lines == 0

    def test_total_code_lines_single_file(self):
        """Test total_code_lines returns correct count for single file."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=70,
                )
            ],
        )
        assert dir_stats.total_code_lines == 70

    def test_total_code_lines_multiple_files(self):
        """Test total_code_lines sums code lines from multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=70,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=50,
                    code_lines=35,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=25,
                    code_lines=20,
                ),
            ],
        )
        assert dir_stats.total_code_lines == 125

    def test_total_code_lines_with_single_subdirectory(self):
        """Test total_code_lines includes code lines from subdirectories."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(
                    path=Path("src/helpers/util1.py"),
                    total_lines=30,
                    code_lines=20,
                ),
                FileStats(
                    path=Path("src/helpers/util2.py"),
                    total_lines=40,
                    code_lines=30,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=70,
                )
            ],
            subdirectories=[subdir],
        )
        assert dir_stats.total_code_lines == 120

    def test_total_code_lines_with_multiple_subdirectories(self):
        """Test total_code_lines sums code lines across multiple subdirectories."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/user.py"),
                    total_lines=80,
                    code_lines=60,
                )
            ],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=60,
                    code_lines=45,
                ),
                FileStats(
                    path=Path("src/views/about.py"),
                    total_lines=40,
                    code_lines=30,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=75,
                )
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_code_lines == 210

    def test_total_code_lines_nested_subdirectories(self):
        """Test total_code_lines recursively counts code lines in nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[
                FileStats(
                    path=Path("src/utils/helpers/helper.py"),
                    total_lines=20,
                    code_lines=15,
                )
            ],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[
                FileStats(
                    path=Path("src/utils/util.py"),
                    total_lines=50,
                    code_lines=40,
                )
            ],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=80,
                )
            ],
            subdirectories=[mid_subdir],
        )
        assert dir_stats.total_code_lines == 135

    def test_total_code_lines_only_subdirectories(self):
        """Test total_code_lines when directory has no direct files."""
        subdir = DirectoryStats(
            path=Path("src/lib"),
            files=[
                FileStats(
                    path=Path("src/lib/lib1.py"),
                    total_lines=75,
                    code_lines=60,
                ),
                FileStats(
                    path=Path("src/lib/lib2.py"),
                    total_lines=125,
                    code_lines=100,
                ),
            ],
        )
        dir_stats = DirectoryStats(path=Path("src"), files=[], subdirectories=[subdir])
        assert dir_stats.total_code_lines == 160

    def test_total_code_lines_complex_structure(self):
        """Test total_code_lines with complex directory structure."""
        subdir1_1 = DirectoryStats(
            path=Path("src/models/entities"),
            files=[
                FileStats(
                    path=Path("src/models/entities/user.py"),
                    total_lines=150,
                    code_lines=120,
                )
            ],
        )
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/base.py"),
                    total_lines=200,
                    code_lines=160,
                )
            ],
            subdirectories=[subdir1_1],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=100,
                    code_lines=75,
                ),
                FileStats(
                    path=Path("src/views/about.py"),
                    total_lines=80,
                    code_lines=60,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=250,
                    code_lines=200,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=50,
                    code_lines=40,
                ),
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_code_lines == 655

    def test_total_code_lines_empty_subdirectories(self):
        """Test total_code_lines with empty subdirectories."""
        subdir1 = DirectoryStats(path=Path("src/empty1"))
        subdir2 = DirectoryStats(path=Path("src/empty2"))
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=80,
                )
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_code_lines == 80

    def test_total_code_lines_files_with_zero_code_lines(self):
        """Test total_code_lines with files containing zero code lines."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/empty1.py"),
                    total_lines=10,
                    code_lines=0,
                ),
                FileStats(
                    path=Path("src/empty2.py"),
                    total_lines=15,
                    code_lines=0,
                ),
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=80,
                ),
            ],
        )
        assert dir_stats.total_code_lines == 80

    def test_total_code_lines_deeply_nested_structure(self):
        """Test total_code_lines with deeply nested directory structure."""
        level3 = DirectoryStats(
            path=Path("src/a/b/c"),
            files=[
                FileStats(
                    path=Path("src/a/b/c/file.py"),
                    total_lines=25,
                    code_lines=20,
                )
            ],
        )
        level2 = DirectoryStats(
            path=Path("src/a/b"),
            files=[
                FileStats(
                    path=Path("src/a/b/file.py"),
                    total_lines=50,
                    code_lines=40,
                )
            ],
            subdirectories=[level3],
        )
        level1 = DirectoryStats(
            path=Path("src/a"),
            files=[
                FileStats(
                    path=Path("src/a/file.py"),
                    total_lines=75,
                    code_lines=60,
                )
            ],
            subdirectories=[level2],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file.py"),
                    total_lines=100,
                    code_lines=80,
                )
            ],
            subdirectories=[level1],
        )
        assert dir_stats.total_code_lines == 200

    def test_total_code_lines_large_numbers(self):
        """Test total_code_lines with large code line counts."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/large1.py"),
                    total_lines=10000,
                    code_lines=8000,
                ),
                FileStats(
                    path=Path("src/large2.py"),
                    total_lines=15000,
                    code_lines=12000,
                ),
                FileStats(
                    path=Path("src/large3.py"),
                    total_lines=20000,
                    code_lines=16000,
                ),
            ],
        )
        assert dir_stats.total_code_lines == 36000

    def test_total_code_lines_mixed_line_types(self):
        """Test total_code_lines with files having mixed line types."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file1.py"),
                    total_lines=100,
                    code_lines=60,
                    comment_lines=25,
                    blank_lines=15,
                ),
                FileStats(
                    path=Path("src/file2.py"),
                    total_lines=150,
                    code_lines=90,
                    comment_lines=40,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/file3.py"),
                    total_lines=80,
                    code_lines=50,
                    comment_lines=20,
                    blank_lines=10,
                ),
            ],
        )
        assert dir_stats.total_code_lines == 200
        # ============================================================================
        # TEST DIRECTORYSTATS - TOTAL_COMMENT_LINES PROPERTY
        # ============================================================================


class TestDirectoryStatsTotalCommentLines:
    """Test suite for DirectoryStats.total_comment_lines property."""

    def test_total_comment_lines_empty_directory(self):
        """Test total_comment_lines returns 0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.total_comment_lines == 0

    def test_total_comment_lines_single_file(self):
        """Test total_comment_lines returns correct count for single file."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=20,
                )
            ],
        )
        assert dir_stats.total_comment_lines == 20

    def test_total_comment_lines_multiple_files(self):
        """Test total_comment_lines sums comment lines from multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=25,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=50,
                    comment_lines=10,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=25,
                    comment_lines=5,
                ),
            ],
        )
        assert dir_stats.total_comment_lines == 40

    def test_total_comment_lines_with_single_subdirectory(
        self,
    ):
        """Test total_comment_lines includes comment lines from subdirectories."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(
                    path=Path("src/helpers/util1.py"),
                    total_lines=30,
                    comment_lines=8,
                ),
                FileStats(
                    path=Path("src/helpers/util2.py"),
                    total_lines=40,
                    comment_lines=12,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=25,
                )
            ],
            subdirectories=[subdir],
        )
        assert dir_stats.total_comment_lines == 45

    def test_total_comment_lines_with_multiple_subdirectories(
        self,
    ):
        """Test total_comment_lines sums comment lines across multiple subdirectories."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/user.py"),
                    total_lines=80,
                    comment_lines=15,
                )
            ],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=60,
                    comment_lines=10,
                ),
                FileStats(
                    path=Path("src/views/about.py"),
                    total_lines=40,
                    comment_lines=8,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=20,
                )
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_comment_lines == 53

    def test_total_comment_lines_nested_subdirectories(
        self,
    ):
        """Test total_comment_lines recursively counts comment lines in nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[
                FileStats(
                    path=Path("src/utils/helpers/helper.py"),
                    total_lines=20,
                    comment_lines=4,
                )
            ],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[
                FileStats(
                    path=Path("src/utils/util.py"),
                    total_lines=50,
                    comment_lines=8,
                )
            ],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=15,
                )
            ],
            subdirectories=[mid_subdir],
        )
        assert dir_stats.total_comment_lines == 27

    def test_total_comment_lines_only_subdirectories(self):
        """Test total_comment_lines when directory has no direct files."""
        subdir = DirectoryStats(
            path=Path("src/lib"),
            files=[
                FileStats(
                    path=Path("src/lib/lib1.py"),
                    total_lines=75,
                    comment_lines=12,
                ),
                FileStats(
                    path=Path("src/lib/lib2.py"),
                    total_lines=125,
                    comment_lines=18,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[],
            subdirectories=[subdir],
        )
        assert dir_stats.total_comment_lines == 30

    def test_total_comment_lines_complex_structure(self):
        """Test total_comment_lines with complex directory structure."""
        subdir1_1 = DirectoryStats(
            path=Path("src/models/entities"),
            files=[
                FileStats(
                    path=Path("src/models/entities/user.py"),
                    total_lines=150,
                    comment_lines=25,
                )
            ],
        )
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/base.py"),
                    total_lines=200,
                    comment_lines=35,
                )
            ],
            subdirectories=[subdir1_1],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=100,
                    comment_lines=20,
                ),
                FileStats(
                    path=Path("src/views/about.py"),
                    total_lines=80,
                    comment_lines=15,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=250,
                    comment_lines=40,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=50,
                    comment_lines=8,
                ),
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_comment_lines == 143

    def test_total_comment_lines_empty_subdirectories(self):
        """Test total_comment_lines with empty subdirectories."""
        subdir1 = DirectoryStats(path=Path("src/empty1"))
        subdir2 = DirectoryStats(path=Path("src/empty2"))
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=18,
                )
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_comment_lines == 18

    def test_total_comment_lines_files_with_zero_comment_lines(
        self,
    ):
        """Test total_comment_lines with files containing zero comment lines."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file1.py"),
                    total_lines=10,
                    comment_lines=0,
                ),
                FileStats(
                    path=Path("src/file2.py"),
                    total_lines=15,
                    comment_lines=0,
                ),
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=22,
                ),
            ],
        )
        assert dir_stats.total_comment_lines == 22

    def test_total_comment_lines_deeply_nested_structure(
        self,
    ):
        """Test total_comment_lines with deeply nested directory structure."""
        level3 = DirectoryStats(
            path=Path("src/a/b/c"),
            files=[
                FileStats(
                    path=Path("src/a/b/c/file.py"),
                    total_lines=25,
                    comment_lines=3,
                )
            ],
        )
        level2 = DirectoryStats(
            path=Path("src/a/b"),
            files=[
                FileStats(
                    path=Path("src/a/b/file.py"),
                    total_lines=50,
                    comment_lines=7,
                )
            ],
            subdirectories=[level3],
        )
        level1 = DirectoryStats(
            path=Path("src/a"),
            files=[
                FileStats(
                    path=Path("src/a/file.py"),
                    total_lines=75,
                    comment_lines=12,
                )
            ],
            subdirectories=[level2],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file.py"),
                    total_lines=100,
                    comment_lines=16,
                )
            ],
            subdirectories=[level1],
        )
        assert dir_stats.total_comment_lines == 38

    def test_total_comment_lines_large_numbers(self):
        """Test total_comment_lines with large comment line counts."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/large1.py"),
                    total_lines=10000,
                    comment_lines=1500,
                ),
                FileStats(
                    path=Path("src/large2.py"),
                    total_lines=15000,
                    comment_lines=2250,
                ),
                FileStats(
                    path=Path("src/large3.py"),
                    total_lines=20000,
                    comment_lines=3000,
                ),
            ],
        )
        assert dir_stats.total_comment_lines == 6750

    def test_total_comment_lines_mixed_line_types(self):
        """Test total_comment_lines with files having mixed line types."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file1.py"),
                    total_lines=100,
                    code_lines=60,
                    comment_lines=25,
                    blank_lines=15,
                ),
                FileStats(
                    path=Path("src/file2.py"),
                    total_lines=150,
                    code_lines=90,
                    comment_lines=40,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/file3.py"),
                    total_lines=80,
                    code_lines=50,
                    comment_lines=20,
                    blank_lines=10,
                ),
            ],
        )
        assert dir_stats.total_comment_lines == 85

    def test_total_comment_lines_well_documented_project(
        self,
    ):
        """Test total_comment_lines with well-documented project (high comment ratio)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file1.py"),
                    total_lines=100,
                    code_lines=40,
                    comment_lines=40,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/file2.py"),
                    total_lines=200,
                    code_lines=80,
                    comment_lines=80,
                    blank_lines=40,
                ),
            ],
        )
        assert dir_stats.total_comment_lines == 120
        # ============================================================================
        # TEST DIRECTORYSTATS - TOTAL_BLANK_LINES PROPERTY
        # ============================================================================


class TestDirectoryStatsTotalBlankLines:
    """Test suite for DirectoryStats.total_blank_lines property."""

    def test_total_blank_lines_empty_directory(
        self,
    ):
        """Test total_blank_lines returns 0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.total_blank_lines == 0

    def test_total_blank_lines_single_file(self):
        """Test total_blank_lines returns correct count for single file."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=15,
                )
            ],
        )
        assert dir_stats.total_blank_lines == 15

    def test_total_blank_lines_multiple_files(self):
        """Test total_blank_lines sums blank lines from multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=50,
                    blank_lines=10,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=25,
                    blank_lines=5,
                ),
            ],
        )
        assert dir_stats.total_blank_lines == 35

    def test_total_blank_lines_with_single_subdirectory(
        self,
    ):
        """Test total_blank_lines includes blank lines from subdirectories."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(
                    path=Path("src/helpers/util1.py"),
                    total_lines=30,
                    blank_lines=6,
                ),
                FileStats(
                    path=Path("src/helpers/util2.py"),
                    total_lines=40,
                    blank_lines=8,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=15,
                )
            ],
            subdirectories=[subdir],
        )
        assert dir_stats.total_blank_lines == 29

    def test_total_blank_lines_with_multiple_subdirectories(
        self,
    ):
        """Test total_blank_lines sums blank lines across multiple subdirectories."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/user.py"),
                    total_lines=80,
                    blank_lines=12,
                )
            ],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=60,
                    blank_lines=10,
                ),
                FileStats(
                    path=Path("src/views/about.py"),
                    total_lines=40,
                    blank_lines=7,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=18,
                )
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_blank_lines == 47

    def test_total_blank_lines_nested_subdirectories(
        self,
    ):
        """Test total_blank_lines recursively counts blank lines in nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[
                FileStats(
                    path=Path("src/utils/helpers/helper.py"),
                    total_lines=20,
                    blank_lines=3,
                )
            ],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[
                FileStats(
                    path=Path("src/utils/util.py"),
                    total_lines=50,
                    blank_lines=8,
                )
            ],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=15,
                )
            ],
            subdirectories=[mid_subdir],
        )
        assert dir_stats.total_blank_lines == 26

    def test_total_blank_lines_only_subdirectories(
        self,
    ):
        """Test total_blank_lines when directory has no direct files."""
        subdir = DirectoryStats(
            path=Path("src/lib"),
            files=[
                FileStats(
                    path=Path("src/lib/lib1.py"),
                    total_lines=75,
                    blank_lines=11,
                ),
                FileStats(
                    path=Path("src/lib/lib2.py"),
                    total_lines=125,
                    blank_lines=19,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[],
            subdirectories=[subdir],
        )
        assert dir_stats.total_blank_lines == 30

    def test_total_blank_lines_complex_structure(
        self,
    ):
        """Test total_blank_lines with complex directory structure."""
        subdir1_1 = DirectoryStats(
            path=Path("src/models/entities"),
            files=[
                FileStats(
                    path=Path("src/models/entities/user.py"),
                    total_lines=150,
                    blank_lines=22,
                )
            ],
        )
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/base.py"),
                    total_lines=200,
                    blank_lines=30,
                )
            ],
            subdirectories=[subdir1_1],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=100,
                    blank_lines=16,
                ),
                FileStats(
                    path=Path("src/views/about.py"),
                    total_lines=80,
                    blank_lines=13,
                ),
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=250,
                    blank_lines=38,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=50,
                    blank_lines=8,
                ),
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_blank_lines == 127

    def test_total_blank_lines_empty_subdirectories(
        self,
    ):
        """Test total_blank_lines with empty subdirectories."""
        subdir1 = DirectoryStats(path=Path("src/empty1"))
        subdir2 = DirectoryStats(path=Path("src/empty2"))
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=14,
                )
            ],
            subdirectories=[subdir1, subdir2],
        )
        assert dir_stats.total_blank_lines == 14

    def test_total_blank_lines_files_with_zero_blank_lines(
        self,
    ):
        """Test total_blank_lines with files containing zero blank lines."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file1.py"),
                    total_lines=10,
                    blank_lines=0,
                ),
                FileStats(
                    path=Path("src/file2.py"),
                    total_lines=15,
                    blank_lines=0,
                ),
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=18,
                ),
            ],
        )
        assert dir_stats.total_blank_lines == 18

    def test_total_blank_lines_deeply_nested_structure(
        self,
    ):
        """Test total_blank_lines with deeply nested directory structure."""
        level3 = DirectoryStats(
            path=Path("src/a/b/c"),
            files=[
                FileStats(
                    path=Path("src/a/b/c/file.py"),
                    total_lines=25,
                    blank_lines=4,
                )
            ],
        )
        level2 = DirectoryStats(
            path=Path("src/a/b"),
            files=[
                FileStats(
                    path=Path("src/a/b/file.py"),
                    total_lines=50,
                    blank_lines=8,
                )
            ],
            subdirectories=[level3],
        )
        level1 = DirectoryStats(
            path=Path("src/a"),
            files=[
                FileStats(
                    path=Path("src/a/file.py"),
                    total_lines=75,
                    blank_lines=12,
                )
            ],
            subdirectories=[level2],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file.py"),
                    total_lines=100,
                    blank_lines=16,
                )
            ],
            subdirectories=[level1],
        )
        assert dir_stats.total_blank_lines == 40

    def test_total_blank_lines_large_numbers(self):
        """Test total_blank_lines with large blank line counts."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/large1.py"),
                    total_lines=10000,
                    blank_lines=1200,
                ),
                FileStats(
                    path=Path("src/large2.py"),
                    total_lines=15000,
                    blank_lines=1800,
                ),
                FileStats(
                    path=Path("src/large3.py"),
                    total_lines=20000,
                    blank_lines=2400,
                ),
            ],
        )
        assert dir_stats.total_blank_lines == 5400

    def test_total_blank_lines_mixed_line_types(
        self,
    ):
        """Test total_blank_lines with files having mixed line types."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/file1.py"),
                    total_lines=100,
                    code_lines=60,
                    comment_lines=25,
                    blank_lines=15,
                ),
                FileStats(
                    path=Path("src/file2.py"),
                    total_lines=150,
                    code_lines=90,
                    comment_lines=40,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/file3.py"),
                    total_lines=80,
                    code_lines=50,
                    comment_lines=20,
                    blank_lines=10,
                ),
            ],
        )
        assert dir_stats.total_blank_lines == 45

    def test_total_blank_lines_compact_code(self):
        """Test total_blank_lines with compact code (few blank lines)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/compact1.py"),
                    total_lines=100,
                    code_lines=85,
                    comment_lines=10,
                    blank_lines=5,
                ),
                FileStats(
                    path=Path("src/compact2.py"),
                    total_lines=200,
                    code_lines=170,
                    comment_lines=25,
                    blank_lines=5,
                ),
            ],
        )
        assert dir_stats.total_blank_lines == 10
        # ============================================================================
        # TEST DIRECTORYSTATS - CODE_PERCENTAGE PROPERTY
        # ============================================================================


class TestDirectoryStatsCodePercentage:
    """Test suite for DirectoryStats.code_percentage property."""

    def test_code_percentage_empty_directory(
        self,
    ):
        """Test code_percentage returns 0.0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.code_percentage == 0.0

    def test_code_percentage_single_file(
        self,
    ):
        """Test code_percentage calculates correctly for single file."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=70,
                )
            ],
        )
        assert dir_stats.code_percentage == 70.0

    def test_code_percentage_multiple_files(
        self,
    ):
        """Test code_percentage calculates correctly across multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=70,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=50,
                    code_lines=35,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=50,
                    code_lines=45,
                ),
            ],
        )
        # Total: 200 lines, 150 code lines = 75%
        assert dir_stats.code_percentage == 75.0

    def test_code_percentage_with_subdirectories(
        self,
    ):
        """Test code_percentage includes subdirectories in calculation."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(
                    path=Path("src/helpers/util1.py"),
                    total_lines=50,
                    code_lines=40,
                )
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=50,
                    code_lines=30,
                )
            ],
            subdirectories=[subdir],
        )
        # Total: 100 lines, 70 code lines = 70%
        assert dir_stats.code_percentage == 70.0

    def test_code_percentage_all_code_lines(
        self,
    ):
        """Test code_percentage returns 100% when all lines are code."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=100,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=50,
                    code_lines=50,
                ),
            ],
        )
        assert dir_stats.code_percentage == 100.0

    def test_code_percentage_no_code_lines(
        self,
    ):
        """Test code_percentage returns 0% when no code lines exist."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/comments.py"),
                    total_lines=100,
                    code_lines=0,
                    comment_lines=100,
                )
            ],
        )
        assert dir_stats.code_percentage == 0.0

    def test_code_percentage_fractional_result(
        self,
    ):
        """Test code_percentage calculates fractional percentages correctly."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=3,
                    code_lines=1,
                )
            ],
        )
        assert dir_stats.code_percentage == pytest.approx(33.333333, rel=1e-5)

    def test_code_percentage_nested_subdirectories(
        self,
    ):
        """Test code_percentage with nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[
                FileStats(
                    path=Path("src/utils/helpers/helper.py"),
                    total_lines=20,
                    code_lines=15,
                )
            ],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[
                FileStats(
                    path=Path("src/utils/util.py"),
                    total_lines=50,
                    code_lines=40,
                )
            ],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=30,
                    code_lines=25,
                )
            ],
            subdirectories=[mid_subdir],
        )
        # Total: 100 lines, 80 code lines = 80%
        assert dir_stats.code_percentage == 80.0

    def test_code_percentage_realistic_project(
        self,
    ):
        """Test code_percentage with realistic project statistics."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=200,
                    code_lines=120,
                    comment_lines=50,
                    blank_lines=30,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=150,
                    code_lines=90,
                    comment_lines=40,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=100,
                    code_lines=70,
                    comment_lines=20,
                    blank_lines=10,
                ),
            ],
        )
        # Total: 450 lines, 280 code lines = 62.222...%
        assert dir_stats.code_percentage == pytest.approx(62.222222, rel=1e-5)

    def test_code_percentage_complex_structure(
        self,
    ):
        """Test code_percentage with complex directory structure."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/user.py"),
                    total_lines=100,
                    code_lines=75,
                )
            ],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=100,
                    code_lines=65,
                )
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    code_lines=80,
                )
            ],
            subdirectories=[
                subdir1,
                subdir2,
            ],
        )
        # Total: 300 lines, 220 code lines = 73.333...%
        assert dir_stats.code_percentage == pytest.approx(73.333333, rel=1e-5)

    def test_code_percentage_zero_total_lines(
        self,
    ):
        """Test code_percentage returns 0.0 when total_lines is 0."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/empty.py"),
                    total_lines=0,
                    code_lines=0,
                )
            ],
        )
        assert dir_stats.code_percentage == 0.0

    def test_code_percentage_high_code_ratio(
        self,
    ):
        """Test code_percentage with high code ratio (minimal comments/blanks)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/compact.py"),
                    total_lines=100,
                    code_lines=90,
                    comment_lines=5,
                    blank_lines=5,
                )
            ],
        )
        assert dir_stats.code_percentage == 90.0

    def test_code_percentage_low_code_ratio(
        self,
    ):
        """Test code_percentage with low code ratio (many comments/blanks)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/documented.py"),
                    total_lines=100,
                    code_lines=30,
                    comment_lines=50,
                    blank_lines=20,
                )
            ],
        )
        assert dir_stats.code_percentage == 30.0
        # ============================================================================
        # TEST DIRECTORYSTATS - COMMENT_PERCENTAGE PROPERTY
        # ============================================================================


class TestDirectoryStatsCommentPercentage:
    """Test suite for DirectoryStats.comment_percentage property."""

    def test_comment_percentage_empty_directory(
        self,
    ):
        """Test comment_percentage returns 0.0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.comment_percentage == 0.0

    def test_comment_percentage_single_file(
        self,
    ):
        """Test comment_percentage calculates correctly for single file."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=20,
                )
            ],
        )
        assert dir_stats.comment_percentage == 20.0

    def test_comment_percentage_multiple_files(
        self,
    ):
        """Test comment_percentage calculates correctly across multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=25,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=50,
                    comment_lines=10,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=50,
                    comment_lines=15,
                ),
            ],
        )
        # Total: 200 lines, 50 comment lines = 25%
        assert dir_stats.comment_percentage == 25.0

    def test_comment_percentage_with_subdirectories(
        self,
    ):
        """Test comment_percentage includes subdirectories in calculation."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(
                    path=Path("src/helpers/util1.py"),
                    total_lines=50,
                    comment_lines=10,
                )
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=50,
                    comment_lines=15,
                )
            ],
            subdirectories=[subdir],
        )
        # Total: 100 lines, 25 comment lines = 25%
        assert dir_stats.comment_percentage == 25.0

    def test_comment_percentage_all_comment_lines(
        self,
    ):
        """Test comment_percentage returns 100% when all lines are comments."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/comments.py"),
                    total_lines=100,
                    comment_lines=100,
                )
            ],
        )
        assert dir_stats.comment_percentage == 100.0

    def test_comment_percentage_no_comment_lines(
        self,
    ):
        """Test comment_percentage returns 0% when no comment lines exist."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/code.py"),
                    total_lines=100,
                    code_lines=100,
                    comment_lines=0,
                )
            ],
        )
        assert dir_stats.comment_percentage == 0.0

    def test_comment_percentage_fractional_result(
        self,
    ):
        """Test comment_percentage calculates fractional percentages correctly."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=3,
                    comment_lines=1,
                )
            ],
        )
        assert dir_stats.comment_percentage == pytest.approx(33.333333, rel=1e-5)

    def test_comment_percentage_nested_subdirectories(
        self,
    ):
        """Test comment_percentage with nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[
                FileStats(
                    path=Path("src/utils/helpers/helper.py"),
                    total_lines=20,
                    comment_lines=4,
                )
            ],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[
                FileStats(
                    path=Path("src/utils/util.py"),
                    total_lines=50,
                    comment_lines=8,
                )
            ],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=30,
                    comment_lines=6,
                )
            ],
            subdirectories=[mid_subdir],
        )
        # Total: 100 lines, 18 comment lines = 18%
        assert dir_stats.comment_percentage == 18.0

    def test_comment_percentage_realistic_project(
        self,
    ):
        """Test comment_percentage with realistic project statistics."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=200,
                    code_lines=120,
                    comment_lines=50,
                    blank_lines=30,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=150,
                    code_lines=90,
                    comment_lines=40,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=100,
                    code_lines=70,
                    comment_lines=20,
                    blank_lines=10,
                ),
            ],
        )
        # Total: 450 lines, 110 comment lines = 24.444...%
        assert dir_stats.comment_percentage == pytest.approx(24.444444, rel=1e-5)

    def test_comment_percentage_complex_structure(
        self,
    ):
        """Test comment_percentage with complex directory structure."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/user.py"),
                    total_lines=100,
                    comment_lines=20,
                )
            ],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=100,
                    comment_lines=15,
                )
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    comment_lines=25,
                )
            ],
            subdirectories=[
                subdir1,
                subdir2,
            ],
        )
        # Total: 300 lines, 60 comment lines = 20%
        assert dir_stats.comment_percentage == 20.0

    def test_comment_percentage_zero_total_lines(
        self,
    ):
        """Test comment_percentage returns 0.0 when total_lines is 0."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/empty.py"),
                    total_lines=0,
                    comment_lines=0,
                )
            ],
        )
        assert dir_stats.comment_percentage == 0.0

    def test_comment_percentage_well_documented_project(
        self,
    ):
        """Test comment_percentage with well-documented project (high comment ratio)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/documented.py"),
                    total_lines=100,
                    code_lines=40,
                    comment_lines=40,
                    blank_lines=20,
                )
            ],
        )
        assert dir_stats.comment_percentage == 40.0

    def test_comment_percentage_poorly_documented_project(
        self,
    ):
        """Test comment_percentage with poorly documented project (low comment ratio)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/undocumented.py"),
                    total_lines=100,
                    code_lines=90,
                    comment_lines=5,
                    blank_lines=5,
                )
            ],
        )
        assert dir_stats.comment_percentage == 5.0
        # ============================================================================
        # TEST DIRECTORYSTATS - BLANK_PERCENTAGE PROPERTY
        # ============================================================================


class TestDirectoryStatsBlankPercentage:
    """Test suite for DirectoryStats.blank_percentage property."""

    def test_blank_percentage_empty_directory(
        self,
    ):
        """Test blank_percentage returns 0.0 for empty directory."""
        dir_stats = DirectoryStats(path=Path("empty_dir"))
        assert dir_stats.blank_percentage == 0.0

    def test_blank_percentage_single_file(
        self,
    ):
        """Test blank_percentage calculates correctly for single file."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=15,
                )
            ],
        )
        assert dir_stats.blank_percentage == 15.0

    def test_blank_percentage_multiple_files(
        self,
    ):
        """Test blank_percentage calculates correctly across multiple files."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=50,
                    blank_lines=10,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=50,
                    blank_lines=10,
                ),
            ],
        )
        # Total: 200 lines, 40 blank lines = 20%
        assert dir_stats.blank_percentage == 20.0

    def test_blank_percentage_with_subdirectories(
        self,
    ):
        """Test blank_percentage includes subdirectories in calculation."""
        subdir = DirectoryStats(
            path=Path("src/helpers"),
            files=[
                FileStats(
                    path=Path("src/helpers/util1.py"),
                    total_lines=50,
                    blank_lines=10,
                )
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=50,
                    blank_lines=15,
                )
            ],
            subdirectories=[subdir],
        )
        # Total: 100 lines, 25 blank lines = 25%
        assert dir_stats.blank_percentage == 25.0

    def test_blank_percentage_all_blank_lines(
        self,
    ):
        """Test blank_percentage returns 100% when all lines are blank."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/blank.py"),
                    total_lines=100,
                    blank_lines=100,
                )
            ],
        )
        assert dir_stats.blank_percentage == 100.0

    def test_blank_percentage_no_blank_lines(
        self,
    ):
        """Test blank_percentage returns 0% when no blank lines exist."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/compact.py"),
                    total_lines=100,
                    code_lines=100,
                    blank_lines=0,
                )
            ],
        )
        assert dir_stats.blank_percentage == 0.0

    def test_blank_percentage_fractional_result(
        self,
    ):
        """Test blank_percentage calculates fractional percentages correctly."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=3,
                    blank_lines=1,
                )
            ],
        )
        assert dir_stats.blank_percentage == pytest.approx(
            33.333333,
            rel=1e-5,
        )

    def test_blank_percentage_nested_subdirectories(
        self,
    ):
        """Test blank_percentage with nested subdirectories."""
        deep_subdir = DirectoryStats(
            path=Path("src/utils/helpers"),
            files=[
                FileStats(
                    path=Path("src/utils/helpers/helper.py"),
                    total_lines=20,
                    blank_lines=3,
                )
            ],
        )
        mid_subdir = DirectoryStats(
            path=Path("src/utils"),
            files=[
                FileStats(
                    path=Path("src/utils/util.py"),
                    total_lines=50,
                    blank_lines=8,
                )
            ],
            subdirectories=[deep_subdir],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=30,
                    blank_lines=4,
                )
            ],
            subdirectories=[mid_subdir],
        )
        # Total: 100 lines, 15 blank lines = 15%
        assert dir_stats.blank_percentage == 15.0

    def test_blank_percentage_realistic_project(
        self,
    ):
        """Test blank_percentage with realistic project statistics."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=200,
                    code_lines=120,
                    comment_lines=50,
                    blank_lines=30,
                ),
                FileStats(
                    path=Path("src/utils.py"),
                    total_lines=150,
                    code_lines=90,
                    comment_lines=40,
                    blank_lines=20,
                ),
                FileStats(
                    path=Path("src/config.py"),
                    total_lines=100,
                    code_lines=70,
                    comment_lines=20,
                    blank_lines=10,
                ),
            ],
        )
        # Total: 450 lines, 60 blank lines = 13.333...%
        assert dir_stats.blank_percentage == pytest.approx(
            13.333333,
            rel=1e-5,
        )

    def test_blank_percentage_complex_structure(
        self,
    ):
        """Test blank_percentage with complex directory structure."""
        subdir1 = DirectoryStats(
            path=Path("src/models"),
            files=[
                FileStats(
                    path=Path("src/models/user.py"),
                    total_lines=100,
                    blank_lines=15,
                )
            ],
        )
        subdir2 = DirectoryStats(
            path=Path("src/views"),
            files=[
                FileStats(
                    path=Path("src/views/home.py"),
                    total_lines=100,
                    blank_lines=20,
                )
            ],
        )
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/main.py"),
                    total_lines=100,
                    blank_lines=10,
                )
            ],
            subdirectories=[
                subdir1,
                subdir2,
            ],
        )
        # Total: 300 lines, 45 blank lines = 15%
        assert dir_stats.blank_percentage == 15.0

    def test_blank_percentage_zero_total_lines(
        self,
    ):
        """Test blank_percentage returns 0.0 when total_lines is 0."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/empty.py"),
                    total_lines=0,
                    blank_lines=0,
                )
            ],
        )
        assert dir_stats.blank_percentage == 0.0

    def test_blank_percentage_compact_code(
        self,
    ):
        """Test blank_percentage with compact code (few blank lines)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/compact.py"),
                    total_lines=100,
                    code_lines=85,
                    comment_lines=10,
                    blank_lines=5,
                )
            ],
        )
        assert dir_stats.blank_percentage == 5.0

    def test_blank_percentage_spacious_code(
        self,
    ):
        """Test blank_percentage with spacious code (many blank lines)."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[
                FileStats(
                    path=Path("src/spacious.py"),
                    total_lines=100,
                    code_lines=50,
                    comment_lines=20,
                    blank_lines=30,
                )
            ],
        )
        assert dir_stats.blank_percentage == 30.0


class TestDirectoryStatsSortFilesBySize:
    """Test suite for DirectoryStats.sort_files_by_size method."""

    def test_sort_files_by_size_basic(
        self,
    ):
        """Test files are sorted by total_lines descending."""
        files = [
            FileStats(
                path=Path("a.py"),
                total_lines=10,
            ),
            FileStats(
                path=Path("b.py"),
                total_lines=30,
            ),
            FileStats(
                path=Path("c.py"),
                total_lines=20,
            ),
        ]
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=files,
        )
        dir_stats.sort_files_by_size()
        assert [f.filename for f in dir_stats.files] == [
            "b.py",
            "c.py",
            "a.py",
        ]

    def test_sort_files_by_size_with_equal_lines(
        self,
    ):
        """Test files with equal total_lines retain relative order."""
        files = [
            FileStats(
                path=Path("a.py"),
                total_lines=10,
            ),
            FileStats(
                path=Path("b.py"),
                total_lines=20,
            ),
            FileStats(
                path=Path("c.py"),
                total_lines=20,
            ),
        ]
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=files,
        )
        dir_stats.sort_files_by_size()
        # b.py and c.py can be in any order, but both before a.py
        assert dir_stats.files[0].total_lines == 20
        assert dir_stats.files[1].total_lines == 20
        assert dir_stats.files[2].total_lines == 10

    def test_sort_files_by_size_empty(
        self,
    ):
        """Test sorting with no files does not fail."""
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=[],
        )
        dir_stats.sort_files_by_size()
        assert dir_stats.files == []

    def test_sort_files_by_size_single_file(
        self,
    ):
        """Test sorting with a single file."""
        files = [
            FileStats(
                path=Path("a.py"),
                total_lines=42,
            )
        ]
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=files,
        )
        dir_stats.sort_files_by_size()
        assert dir_stats.files[0].filename == "a.py"

    def test_sort_files_by_size_with_subdirectories(
        self,
    ):
        """Test sorting is applied recursively to subdirectories."""
        sub_files = [
            FileStats(
                path=Path("sub1.py"),
                total_lines=5,
            ),
            FileStats(
                path=Path("sub2.py"),
                total_lines=15,
            ),
            FileStats(
                path=Path("sub3.py"),
                total_lines=10,
            ),
        ]
        subdir = DirectoryStats(
            path=Path("src/sub"),
            files=sub_files,
        )
        files = [
            FileStats(
                path=Path("a.py"),
                total_lines=8,
            ),
            FileStats(
                path=Path("b.py"),
                total_lines=3,
            ),
        ]
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=files,
            subdirectories=[subdir],
        )
        dir_stats.sort_files_by_size()
        # Check root directory sorted
        assert [f.filename for f in dir_stats.files] == [
            "a.py",
            "b.py",
        ]
        # Check subdirectory sorted
        assert [f.filename for f in subdir.files] == [
            "sub2.py",
            "sub3.py",
            "sub1.py",
        ]

    def test_sort_files_by_size_deeply_nested(
        self,
    ):
        """Test sorting works for deeply nested subdirectories."""
        deep_files = [
            FileStats(
                path=Path("deep1.py"),
                total_lines=2,
            ),
            FileStats(
                path=Path("deep2.py"),
                total_lines=7,
            ),
        ]
        deep_subdir = DirectoryStats(
            path=Path("src/deep"),
            files=deep_files,
        )
        mid_subdir = DirectoryStats(
            path=Path("src/mid"),
            files=[],
            subdirectories=[deep_subdir],
        )
        root_files = [
            FileStats(
                path=Path("root1.py"),
                total_lines=1,
            ),
            FileStats(
                path=Path("root2.py"),
                total_lines=5,
            ),
        ]
        dir_stats = DirectoryStats(
            path=Path("src"),
            files=root_files,
            subdirectories=[mid_subdir],
        )
        dir_stats.sort_files_by_size()
        assert [f.filename for f in dir_stats.files] == [
            "root2.py",
            "root1.py",
        ]
        assert [f.filename for f in deep_subdir.files] == [
            "deep2.py",
            "deep1.py",
        ]

        class TestDirectoryStatsStr:
            """Test suite for DirectoryStats.__str__ method."""

            def test_str_empty_directory(self):
                dir_stats = DirectoryStats(path=Path("empty_dir"))
                expected = "empty_dir: 0 files, 0 lines (0 code, 0 comments, 0 blank)"
                assert str(dir_stats) == expected

            def test_str_single_file(self):
                dir_stats = DirectoryStats(
                    path=Path("src"),
                    files=[
                        FileStats(
                            path=Path("src/main.py"),
                            total_lines=10,
                            code_lines=7,
                            comment_lines=2,
                            blank_lines=1,
                        )
                    ],
                )
                expected = "src: 1 files, 10 lines (7 code, 2 comments, 1 blank)"
                assert str(dir_stats) == expected

            def test_str_multiple_files(self):
                dir_stats = DirectoryStats(
                    path=Path("src"),
                    files=[
                        FileStats(
                            path=Path("src/a.py"),
                            total_lines=10,
                            code_lines=7,
                            comment_lines=2,
                            blank_lines=1,
                        ),
                        FileStats(
                            path=Path("src/b.py"),
                            total_lines=20,
                            code_lines=15,
                            comment_lines=3,
                            blank_lines=2,
                        ),
                    ],
                )
                expected = "src: 2 files, 30 lines (22 code, 5 comments, 3 blank)"
                assert str(dir_stats) == expected

            def test_str_with_subdirectories(self):
                subdir = DirectoryStats(
                    path=Path("src/utils"),
                    files=[
                        FileStats(
                            path=Path("src/utils/util.py"),
                            total_lines=5,
                            code_lines=3,
                            comment_lines=1,
                            blank_lines=1,
                        )
                    ],
                )
                dir_stats = DirectoryStats(
                    path=Path("src"),
                    files=[
                        FileStats(
                            path=Path("src/main.py"),
                            total_lines=10,
                            code_lines=7,
                            comment_lines=2,
                            blank_lines=1,
                        )
                    ],
                    subdirectories=[subdir],
                )
                expected = "src: 2 files, 15 lines (10 code, 3 comments, 2 blank)"
                assert str(dir_stats) == expected

            def test_str_nested_subdirectories(self):
                deep_subdir = DirectoryStats(
                    path=Path("src/a/b"),
                    files=[
                        FileStats(
                            path=Path("src/a/b/file.py"),
                            total_lines=3,
                            code_lines=2,
                            comment_lines=1,
                            blank_lines=0,
                        )
                    ],
                )
                subdir = DirectoryStats(
                    path=Path("src/a"),
                    files=[
                        FileStats(
                            path=Path("src/a/file.py"),
                            total_lines=4,
                            code_lines=3,
                            comment_lines=1,
                            blank_lines=0,
                        )
                    ],
                    subdirectories=[deep_subdir],
                )
                dir_stats = DirectoryStats(
                    path=Path("src"),
                    files=[
                        FileStats(
                            path=Path("src/main.py"),
                            total_lines=5,
                            code_lines=4,
                            comment_lines=1,
                            blank_lines=0,
                        )
                    ],
                    subdirectories=[subdir],
                )
                expected = "src: 3 files, 12 lines (9 code, 3 comments, 0 blank)"
                assert str(dir_stats) == expected

            def test_str_directory_with_no_name(self):
                dir_stats = DirectoryStats(path=Path(""))
                expected = ": 0 files, 0 lines (0 code, 0 comments, 0 blank)"
                assert str(dir_stats) == expected

            def test_str_directory_with_special_characters(self):
                dir_stats = DirectoryStats(path=Path("my project!"))
                expected = "my project!: 0 files, 0 lines (0 code, 0 comments, 0 blank)"
                assert str(dir_stats) == expected
