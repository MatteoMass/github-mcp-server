import requests
import re
import os
from typing import List, Dict, Tuple

def parse_repo_url(url: str) -> Tuple[str, str, str, str]:
    url = url.rstrip('/')
    pattern = r'^https:\/\/github\.com\/([^\/]+)\/([^\/]+)(\/tree\/([^\/]+)(\/(.+))?)?$'
    match = re.match(pattern, url)
    if not match:
        raise ValueError('Invalid GitHub repository URL format.')
    return match[1], match[2], match[4] or '', match[6] or ''

def fetch_repo_sha(owner: str, repo: str, ref: str, path: str, token: str) -> str:
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}' if ref else f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Accept': 'application/vnd.github.object+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 403 and resp.headers.get('X-RateLimit-Remaining') == '0':
        raise Exception('GitHub API rate limit exceeded.')
    if resp.status_code == 404:
        raise Exception('Repository, branch, or path not found.')
    if not resp.ok:
        raise Exception(f'Failed to fetch SHA. Status: {resp.status_code}')
    return resp.json()['sha']

def fetch_repo_tree(owner: str, repo: str, sha: str, token: str) -> List[Dict]:
    url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}?recursive=1'
    headers = {'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 403 and resp.headers.get('X-RateLimit-Remaining') == '0':
        raise Exception('GitHub API rate limit exceeded.')
    if not resp.ok:
        raise Exception(f'Failed to fetch repo tree. Status: {resp.status_code}')
    return resp.json()['tree']

def fetch_file_contents(files: List[Dict], token: str) -> List[Dict]:
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    if token:
        headers['Authorization'] = f'token {token}'
    contents = []
    for file in files:
        resp = requests.get(file['url'], headers=headers)
        if not resp.ok:
            raise Exception(f'Failed to fetch file: {file["path"]} (status {resp.status_code})')
        contents.append({'path': file['path'], 'text': resp.text})
    return contents

def build_tree_structure(paths: List[str]) -> Dict:
    tree = {}
    for path in paths:
        parts = path.split('/')
        current = tree
        for i, part in enumerate(parts):
            if part not in current:
                current[part] = {} if i < len(parts) - 1 else None
            current = current[part] if current[part] is not None else {}
    return tree

def format_tree_index(tree: Dict, prefix: str = '') -> str:
    output = ''
    entries = list(tree.items())
    for i, (name, sub_tree) in enumerate(entries):
        is_last = i == len(entries) - 1
        line_prefix = '└── ' if is_last else '├── '
        child_prefix = '    ' if is_last else '│   '
        output += f"{prefix}{line_prefix}{name}\n"
        if sub_tree:
            output += format_tree_index(sub_tree, prefix + child_prefix)
    return output

def format_repo_contents(contents: List[Dict]) -> str:
    contents.sort(key=lambda x: x['path'].lower())
    paths = [item['path'] for item in contents]
    tree = build_tree_structure(paths)
    index = format_tree_index(tree)
    result = f"Directory Structure:\n\n{index}"
    for item in contents:
        result += f"\n\n---\nFile: {item['path']}\n---\n\n{item['text']}\n"
    return result