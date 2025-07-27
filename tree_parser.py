import os
from typing import Tuple, Dict

RELEVANT_EXTENSIONS = {'.py', '.js', '.md'}


def parse_repo(repo_path: str) -> Tuple[str, Dict[str, str], str]:
    file_tree_lines = []
    file_contents = {}
    readme_content = ''
    for root, dirs, files in os.walk(repo_path):
        rel_root = os.path.relpath(root, repo_path)
        for file in files:
            rel_path = os.path.normpath(os.path.join(rel_root, file)) if rel_root != '.' else file
            file_tree_lines.append(rel_path)
            ext = os.path.splitext(file)[1].lower()
            if ext in RELEVANT_EXTENSIONS:
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read(2000)  # Limit to 2000 chars per file
                        file_contents[rel_path] = content
                except Exception:
                    pass
            if file.lower().startswith('readme'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        readme_content = f.read(4000)
                except Exception:
                    pass
    file_tree = '\n'.join(sorted(file_tree_lines))
    return file_tree, file_contents, readme_content 