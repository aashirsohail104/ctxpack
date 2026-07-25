# ctxpack — Context packing tool for AI coding assistants
# Python 3.10+, standard library only

import argparse
import json
import math
import os
import sys

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_FILE_SIZE = 1_048_576  # 1 MB

NOISE_DIRS = frozenset({
    '.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env',
    '.eggs', 'dist', 'build', 'target', '.next', '.nuxt',
    '.idea', '.vscode', '.svn', '.hg', '.mypy_cache', '.pytest_cache',
    '.ruff_cache', '.hypothesis',
})

NOISE_FILES = frozenset({
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'Gemfile.lock', 'poetry.lock', 'Cargo.lock',
    'composer.lock', 'flake.lock',
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
})

NOISE_EXTENSIONS = frozenset({
    '.pyc', '.pyo',
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp',
    '.ico', '.icns',
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z', '.zst',
    '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm',
    '.wav', '.flac', '.ogg', '.m4a',
    '.o', '.obj', '.class', '.jar', '.war',
    '.exe', '.dll', '.so', '.dylib', '.bin',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.wasm', '.map',
})

NOISE_DIR_REASONS = {
    '.git': 'Version control directory',
    'node_modules': 'Dependency directory',
    '__pycache__': 'Python cache directory',
    '.venv': 'Virtual environment',
    'venv': 'Virtual environment',
    'env': 'Virtual environment',
    '.eggs': 'Python egg directory',
    'dist': 'Build artifact',
    'build': 'Build artifact',
    'target': 'Build artifact',
    '.next': 'Build artifact',
    '.nuxt': 'Build artifact',
    '.idea': 'IDE metadata directory',
    '.vscode': 'IDE metadata directory',
    '.svn': 'Version control directory',
    '.hg': 'Version control directory',
    '.mypy_cache': 'Type checking cache',
    '.pytest_cache': 'Testing cache',
    '.ruff_cache': 'Linting cache',
    '.hypothesis': 'Testing cache',
}

EXTENSION_SCORES = {
    '.py': 10, '.js': 10, '.ts': 10, '.jsx': 10, '.tsx': 10,
    '.go': 10, '.rs': 10, '.java': 10, '.kt': 10, '.scala': 10,
    '.c': 10, '.cpp': 10, '.h': 10, '.hpp': 10,
    '.rb': 9, '.php': 9, '.swift': 9,
    '.sh': 8, '.bash': 8, '.zsh': 8, '.ps1': 8, '.bat': 8,
    '.md': 7, '.rst': 7, '.tex': 7,
    '.yaml': 5, '.yml': 5, '.toml': 5, '.cfg': 5, '.ini': 5, '.conf': 5,
    '.css': 4, '.scss': 4, '.less': 4, '.html': 4, '.svelte': 4,
    '.vue': 4,
    '.json': 3, '.xml': 3, '.csv': 3,
    '.sql': 6,
    '.dockerfile': 6, '.dockerignore': 6,
    '.gitignore': 5, '.gitattributes': 5,
    '.env': 5, '.env.example': 5,
}

EXT_TO_LANG = {
    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
    '.jsx': 'javascript', '.tsx': 'typescript',
    '.go': 'go', '.rs': 'rust', '.java': 'java', '.kt': 'kotlin',
    '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
    '.rb': 'ruby', '.php': 'php', '.swift': 'swift',
    '.sh': 'bash', '.bash': 'bash', '.zsh': 'bash', '.ps1': 'powershell',
    '.md': 'markdown', '.rst': 'rst', '.tex': 'latex',
    '.yaml': 'yaml', '.yml': 'yaml', '.toml': 'toml',
    '.css': 'css', '.scss': 'scss', '.less': 'less',
    '.html': 'html', '.svelte': 'html', '.vue': 'html',
    '.json': 'json', '.xml': 'xml', '.sql': 'sql',
    '.dockerfile': 'dockerfile',
    '.env': 'text', '.gitignore': 'gitignore',
}

STOPWORDS = frozenset({
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'by', 'with', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'shall', 'can', 'need',
    'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their',
    'we', 'our', 'you', 'your', 'he', 'she', 'him', 'her', 'his',
    'not', 'no', 'nor', 'if', 'so', 'than', 'too', 'very', 'just',
    'about', 'above', 'after', 'again', 'all', 'also', 'any', 'because',
    'before', 'between', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'only', 'own', 'same', 'into', 'over', 'under',
    'up', 'down', 'out', 'off', 'then', 'once', 'here', 'there',
    'when', 'where', 'why', 'how', 'which', 'who', 'whom', 'what',
})

TREE_BRANCH = '\u251c\u2500\u2500 '
TREE_LAST = '\u2514\u2500\u2500 '
TREE_PIPE = '\u2502   '
TREE_SPACE = '    '

# ---------------------------------------------------------------------------
# Token counting
# ---------------------------------------------------------------------------

def count_tokens(text):
    return math.ceil(len(text) / 4)

# ---------------------------------------------------------------------------
# Noise detection
# ---------------------------------------------------------------------------

def is_noise_dir(name):
    return name in NOISE_DIRS

def get_noise_dir_reason(name):
    return NOISE_DIR_REASONS.get(name, 'Build/dependency artifact')

def is_noise_file(name):
    if name in NOISE_FILES:
        return True
    _, ext = os.path.splitext(name)
    if ext.lower() in NOISE_EXTENSIONS:
        return True
    return False

def get_noise_file_reason(name):
    if name in NOISE_FILES:
        if 'lock' in name.lower():
            return 'Lockfile -- auto-generated'
        return 'IDE/OS metadata file'
    _, ext = os.path.splitext(name)
    if ext.lower() in NOISE_EXTENSIONS:
        ext_lower = ext.lower()
        if ext_lower in ('.pyc', '.pyo'):
            return 'Python bytecode'
        if ext_lower in ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.ico', '.icns', '.svg'):
            return 'Image file'
        if ext_lower in ('.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.wav', '.flac', '.ogg', '.m4a'):
            return 'Media file'
        if ext_lower in ('.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z', '.zst'):
            return 'Archive file'
        if ext_lower in ('.exe', '.dll', '.so', '.dylib', '.bin'):
            return 'Binary file'
        if ext_lower in ('.o', '.obj', '.class', '.jar', '.war'):
            return 'Compiled artifact'
        if ext_lower in ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'):
            return 'Document file'
        if ext_lower in ('.ttf', '.otf', '.woff', '.woff2', '.eot'):
            return 'Font file'
        if ext_lower in ('.wasm',):
            return 'WebAssembly binary'
        if ext_lower in ('.map',):
            return 'Source map'
        return 'Binary/artifact file'
    return 'Unknown noise file'

# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def scan_files(root_path):
    included = []
    excluded = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        rel_dir = os.path.relpath(dirpath, root_path)
        if rel_dir == '.':
            rel_dir = ''

        filtered_dirs = []
        for d in dirnames:
            if is_noise_dir(d):
                excluded.append({
                    'path': os.path.join(rel_dir, d) if rel_dir else d,
                    'reason': get_noise_dir_reason(d),
                })
            else:
                filtered_dirs.append(d)
        dirnames[:] = filtered_dirs

        for filename in filenames:
            rel_path = os.path.join(rel_dir, filename) if rel_dir else filename
            full_path = os.path.join(dirpath, filename)

            if is_noise_file(filename):
                excluded.append({
                    'path': rel_path,
                    'reason': get_noise_file_reason(filename),
                })
                continue

            try:
                size = os.path.getsize(full_path)
            except OSError as e:
                excluded.append({
                    'path': rel_path,
                    'reason': f'Unreadable: {e}',
                })
                continue

            if size > MAX_FILE_SIZE:
                excluded.append({
                    'path': rel_path,
                    'reason': 'Large file (>1 MB) -- may be generated',
                })
                continue

            included.append({
                'path': rel_path,
                'full_path': full_path,
                'size': size,
            })

    included.sort(key=lambda x: x['path'])
    excluded.sort(key=lambda x: x['path'])
    return included, excluded

# ---------------------------------------------------------------------------
# File reading
# ---------------------------------------------------------------------------

def read_file(full_path):
    try:
        with open(full_path, 'r', encoding='utf-8', errors='strict') as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None

def is_minified(content):
    return '\n' not in content.rstrip('\n') and len(content) > 5000

# ---------------------------------------------------------------------------
# Task parsing
# ---------------------------------------------------------------------------

def parse_task(task_desc):
    tokens = task_desc.lower().split()
    return {t for t in tokens if len(t) >= 3 and t not in STOPWORDS}

# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------

def get_extension_score(filepath):
    _, ext = os.path.splitext(filepath)
    return EXTENSION_SCORES.get(ext.lower(), 2)

def rank_files(included_files, task_keywords, root_path):
    if not task_keywords:
        ranked = []
        for f in included_files:
            content = read_file(f['full_path'])
            if content is None:
                continue
            if is_minified(content):
                continue
            ranked.append((f['path'], content, 0.0, count_tokens(content)))
        ranked.sort(key=lambda x: (x[0],))
        return ranked

    scored = []
    for f in included_files:
        content = read_file(f['full_path'])
        if content is None:
            continue
        if is_minified(content):
            continue

        content_lower = content.lower()
        content_len = len(content_lower)
        if content_len == 0:
            keyword_ratio = 0.0
        else:
            match_count = sum(content_lower.count(kw) for kw in task_keywords)
            keyword_ratio = match_count / content_len

        ext_score = get_extension_score(f['path'])
        final_score = (keyword_ratio * 0.6) + ((ext_score / 10.0) * 0.4)

        token_count = count_tokens(content)
        scored.append((f['path'], content, final_score, token_count))

    scored.sort(key=lambda x: (-x[2], x[0]))
    return scored

# ---------------------------------------------------------------------------
# Directory tree
# ---------------------------------------------------------------------------

def build_tree(root_path):
    root_name = os.path.basename(os.path.abspath(root_path))
    lines = [f'{root_name}/']

    def _walk(dirpath, prefix, is_last_stack):
        try:
            entries = sorted(os.listdir(dirpath))
        except OSError:
            return

        filtered = []
        for e in entries:
            full = os.path.join(dirpath, e)
            if os.path.isdir(full) and is_noise_dir(e):
                continue
            if not os.path.isdir(full) and is_noise_file(e):
                continue
            filtered.append(e)

        for i, entry in enumerate(filtered):
            is_last = (i == len(filtered) - 1)
            is_last_stack.append(is_last)

            if os.path.isdir(os.path.join(dirpath, entry)):
                connector = TREE_LAST if is_last else TREE_BRANCH
                lines.append(f'{prefix}{connector}{entry}/')
                sub_prefix = prefix + (TREE_SPACE if is_last else TREE_PIPE)
                _walk(os.path.join(dirpath, entry), sub_prefix, is_last_stack)
            else:
                connector = TREE_LAST if is_last else TREE_BRANCH
                lines.append(f'{prefix}{connector}{entry}')

            is_last_stack.pop()

    _walk(root_path, '', [])
    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# Bundling
# ---------------------------------------------------------------------------

def bundle_files(ranked_files, budget, tree_str, task_desc, root_path):
    project_name = os.path.basename(os.path.abspath(root_path))

    header = f'# ctxpack bundle -- {project_name}\n\n'
    task_section = f'## Task\n\n{task_desc}\n\n'

    base = header + task_section
    base_tokens = count_tokens(base)

    if base_tokens > budget:
        bundle = base[:max(1, budget * 4)]
        return bundle, budget - count_tokens(bundle), [], [], False

    bundle_parts = [header, task_section]
    remaining = budget - base_tokens
    included = []
    excluded = []
    tree_included = False

    tree_full = f'## Project Structure\n\n```\n{tree_str}\n```\n\n'
    tree_cost = count_tokens(tree_full)

    if tree_cost <= remaining and budget >= 500:
        bundle_parts.append(tree_full)
        remaining -= tree_cost
        tree_included = True
    elif tree_cost > remaining:
        excluded.append({
            'path': '<directory tree>',
            'reason': f'Tree too large ({tree_cost} tokens) for remaining budget ({remaining} tokens)',
        })

    for file_path, content, score, content_tokens in ranked_files:
        _, ext = os.path.splitext(file_path)
        lang = EXT_TO_LANG.get(ext.lower(), '')

        file_header = f'### {file_path}\n\n'
        code_start = f'```{lang}\n'
        code_end = '\n```\n\n'

        overhead = count_tokens(file_header + code_start + code_end)

        if content_tokens + overhead <= remaining:
            section = file_header + code_start + content + code_end
            section_tokens = count_tokens(section)
            bundle_parts.append(section)
            remaining -= section_tokens
            included.append({
                'path': file_path,
                'tokens': section_tokens,
                'reason': f'Relevance score: {score:.4f}',
            })
        elif overhead < remaining:
            overhead_str = file_header + code_start + '\n[... TRUNCATED ...]\n' + code_end
            max_content_chars = remaining * 4 - len(overhead_str)
            if max_content_chars > 0:
                truncated = content[:max_content_chars]
                section = file_header + code_start + truncated + '\n[... TRUNCATED ...]\n' + code_end
                section_tokens = count_tokens(section)
                bundle_parts.append(section)
                remaining -= section_tokens
                included.append({
                    'path': file_path,
                    'tokens': section_tokens,
                    'truncated': True,
                    'reason': 'Head-only truncation: file too large for remaining budget',
                })
            else:
                excluded.append({
                    'path': file_path,
                    'reason': 'File overhead exceeds remaining budget',
                })
        else:
            excluded.append({
                'path': file_path,
                'reason': 'File too large for remaining budget',
            })

    bundle = ''.join(bundle_parts)
    used = count_tokens(bundle)
    return bundle, used, included, excluded, tree_included

# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def build_manifest(budget, used, included, excluded, task_desc):
    manifest = {
        'budget': budget,
        'used': used,
        'included': included,
        'excluded': excluded,
        'task': task_desc,
    }
    manifest['included'].sort(key=lambda x: x['path'])
    manifest['excluded'].sort(key=lambda x: x['path'])
    return manifest

def one_line_summary(included_count, used, budget, excluded_count):
    return f'ctxpack: {included_count} files included ({used}/{budget} tokens), {excluded_count} files excluded\n'

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class CtxArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'Error: {message}\n')
        self.exit(1)

def parse_args(argv=None):
    parser = CtxArgumentParser(
        prog='ctxpack',
        description='Pack relevant project files into a token-budgeted markdown bundle.',
        add_help=False,
    )
    parser.add_argument('--path', required=True, help='Folder to pack')
    parser.add_argument('--task', required=True, help='Task description for relevance ranking')
    parser.add_argument('--budget', required=True, help='Maximum token budget for the bundle')
    parser.add_argument('--out', required=False, default=None, help='Write bundle to file (default: stdout)')
    parser.add_argument('--manifest', required=False, default=None, help='Write manifest JSON to file')

    args = parser.parse_args(argv)

    try:
        args.budget = int(args.budget)
    except (ValueError, TypeError):
        sys.stderr.write('Error: --budget must be a positive integer\n')
        sys.exit(1)

    if args.budget <= 0:
        sys.stderr.write('Error: --budget must be a positive integer\n')
        sys.exit(1)

    if not os.path.exists(args.path):
        sys.stderr.write(f'Error: Path not found: {args.path}\n')
        sys.exit(2)

    if not os.path.isdir(args.path):
        sys.stderr.write(f'Error: Path is not a directory: {args.path}\n')
        sys.exit(2)

    args.path = os.path.abspath(args.path)
    return args

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    try:
        included_files, excluded_from_scan = scan_files(args.path)
    except OSError as e:
        sys.stderr.write(f'Error: Cannot read path: {args.path} -- {e}\n')
        sys.exit(2)

    task_keywords = parse_task(args.task)
    ranked = rank_files(included_files, task_keywords, args.path)

    tree_str = build_tree(args.path)

    bundle, used, included_in_bundle, excluded_from_bundle, tree_included = bundle_files(
        ranked, args.budget, tree_str, args.task, args.path
    )

    all_excluded = excluded_from_scan + excluded_from_bundle

    manifest_included = []
    for entry in included_in_bundle:
        me = {
            'path': entry['path'],
            'tokens': entry['tokens'],
            'reason': entry['reason'],
        }
        if entry.get('truncated'):
            me['truncated'] = True
        manifest_included.append(me)

    if not tree_included:
        all_excluded.append({
            'path': '<directory tree>',
            'reason': 'Excluded to stay within budget (budget too small or tree too large)',
        })

    if args.out:
        try:
            with open(args.out, 'w', encoding='utf-8') as f:
                f.write(bundle)
        except OSError as e:
            sys.stderr.write(f'Error: Cannot write to --out: {args.out} -- {e}\n')
            sys.exit(1)
    else:
        try:
            sys.stdout.write(bundle)
        except UnicodeEncodeError:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stdout.write(bundle)

    if args.manifest:
        manifest = build_manifest(args.budget, used, manifest_included, all_excluded, args.task)
        try:
            with open(args.manifest, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
                f.write('\n')
        except OSError as e:
            sys.stderr.write(f'Error: Cannot write to --manifest: {args.manifest} -- {e}\n')
            sys.exit(1)
    else:
        sys.stderr.write(one_line_summary(
            len(manifest_included), used, args.budget, len(all_excluded)
        ))

    sys.exit(0)

if __name__ == '__main__':
    main()
