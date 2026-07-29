"""Constants used by the ctxpack pipeline.

All noise patterns, extension scores, language hints, and stopwords live
here so they can be reviewed and tuned in one place.
"""

MAX_FILE_SIZE = 1_048_576  # 1 MB

NOISE_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env", ".eggs",
    "dist", "build", "target", ".next", ".nuxt", ".idea", ".vscode",
    ".svn", ".hg", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".hypothesis",
})

NOISE_FILES = frozenset({
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Gemfile.lock",
    "poetry.lock", "Cargo.lock", "composer.lock", "flake.lock",
    ".DS_Store", "Thumbs.db", "desktop.ini",
})

NOISE_EXTENSIONS = frozenset({
    ".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff",
    ".webp", ".ico", ".icns", ".zip", ".tar", ".gz", ".bz2", ".xz",
    ".rar", ".7z", ".zst", ".mp3", ".mp4", ".avi", ".mov", ".wmv",
    ".flv", ".mkv", ".webm", ".wav", ".flac", ".ogg", ".m4a", ".o",
    ".obj", ".class", ".jar", ".war", ".exe", ".dll", ".so", ".dylib",
    ".bin", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".ttf", ".otf", ".woff", ".woff2", ".eot", ".wasm", ".map",
})

NOISE_DIR_REASONS = {
    ".git": "Version control directory",
    "node_modules": "Dependency directory",
    "__pycache__": "Python cache directory",
    ".venv": "Virtual environment",
    "venv": "Virtual environment",
    "env": "Virtual environment",
    ".eggs": "Python egg directory",
    "dist": "Build artifact",
    "build": "Build artifact",
    "target": "Build artifact",
    ".next": "Build artifact",
    ".nuxt": "Build artifact",
    ".idea": "IDE metadata directory",
    ".vscode": "IDE metadata directory",
    ".svn": "Version control directory",
    ".hg": "Version control directory",
    ".mypy_cache": "Type checking cache",
    ".pytest_cache": "Testing cache",
    ".ruff_cache": "Linting cache",
    ".hypothesis": "Testing cache",
}

EXTENSION_SCORES = {
    ".py": 10, ".js": 10, ".ts": 10, ".jsx": 10, ".tsx": 10,
    ".go": 10, ".rs": 10, ".java": 10, ".kt": 10, ".scala": 10,
    ".c": 10, ".cpp": 10, ".h": 10, ".hpp": 10,
    ".rb": 9, ".php": 9, ".swift": 9,
    ".sh": 8, ".bash": 8, ".zsh": 8, ".ps1": 8, ".bat": 8,
    ".md": 7, ".rst": 7, ".txt": 7, ".tex": 7,
    ".sql": 6, ".dockerfile": 6, ".dockerignore": 6,
    ".yaml": 5, ".yml": 5, ".toml": 5, ".cfg": 5, ".ini": 5,
    ".conf": 5, ".gitignore": 5, ".gitattributes": 5,
    ".env": 5, ".env.example": 5,
    ".css": 4, ".scss": 4, ".less": 4, ".html": 4, ".svelte": 4, ".vue": 4,
    ".json": 3, ".xml": 3, ".csv": 3,
}

FILENAME_SCORES = {"makefile": 6, "dockerfile": 6}

EXT_TO_LANG = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".jsx": "javascript", ".tsx": "typescript", ".go": "go", ".rs": "rust",
    ".java": "java", ".kt": "kotlin", ".c": "c", ".cpp": "cpp", ".h": "c",
    ".hpp": "cpp", ".rb": "ruby", ".php": "php", ".swift": "swift",
    ".sh": "bash", ".bash": "bash", ".zsh": "bash", ".ps1": "powershell",
    ".md": "markdown", ".rst": "rst", ".tex": "latex",
    ".yaml": "yaml", ".yml": "yaml", ".toml": "toml",
    ".css": "css", ".scss": "scss", ".less": "less",
    ".html": "html", ".svelte": "html", ".vue": "html",
    ".json": "json", ".xml": "xml", ".sql": "sql",
    ".dockerfile": "dockerfile", ".env": "text", ".gitignore": "gitignore",
}

STOPWORDS = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "by", "with", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "this", "that", "these", "those", "it", "its", "they", "them", "their",
    "we", "our", "you", "your", "he", "she", "him", "her", "his", "not",
    "no", "nor", "if", "so", "than", "too", "very", "just", "about",
    "above", "after", "again", "all", "also", "any", "because", "before",
    "between", "both", "each", "few", "more", "most", "other", "some",
    "such", "only", "own", "same", "into", "over", "under", "up", "down",
    "out", "off", "then", "once", "here", "there", "when", "where", "why",
    "how", "which", "who", "whom", "what",
})

# Tree-drawing glyphs (Unicode box-drawing).
TREE_BRANCH = "├── "
TREE_LAST = "└── "
TREE_PIPE = "│   "
TREE_SPACE = "    "

# Truncation marker — written when a file is too large for the remaining budget.
TRUNCATION_MARKER = "\n[... TRUNCATED: file exceeds remaining budget ...]\n"
