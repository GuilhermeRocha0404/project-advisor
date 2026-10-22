"""Prepare one advisor workspace. Preview first; never overwrite project state."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.0.0'
MANIFEST = '.advisor-workspace.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    fd, temp = tempfile.mkstemp(prefix='.advisor-write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def prepare(args):
    workspace = Path(args.workspace).expanduser().resolve()
    project = Path(args.project).expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError('Project must be a directory.')
    if workspace == project or workspace in project.parents or project in workspace.parents:
        raise ValueError('Advisor and target project must have separate directory trees.')
    if workspace == ROOT or ROOT in workspace.parents:
        raise ValueError('State must be outside the installed skill.')
    if args.state_file not in ('ADVISOR_STATE.md', 'CONSULTOR_STATE.md'):
        raise ValueError('Unsupported state filename.')
    manifest_path = workspace / MANIFEST
    if manifest_path.is_symlink():
        raise ValueError('Manifest cannot be a symlink.')
    previous = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else None
    if previous:
        if previous.get('schema') != 1:
            raise ValueError('Unsupported manifest schema.')
        if Path(previous['project']).resolve() != project:
            raise ValueError('Workspace belongs to another project. Use a new folder.')
        if previous['state_file'] != args.state_file:
            raise ValueError('Preserve the existing state filename.')
        if previous['harness'] != args.harness:
            raise ValueError('Harness change requires manual review of existing adapters.')
    state = workspace / args.state_file
    other = workspace / ('CONSULTOR_STATE.md' if args.state_file == 'ADVISOR_STATE.md' else 'ADVISOR_STATE.md')
    if other.exists():
        raise ValueError('Another state exists. Resolve it explicitly; do not create competing states.')
    if state.is_symlink():
        raise ValueError('State cannot be a symlink.')
    if previous and not state.exists():
        raise ValueError('Existing workspace state is missing. Recover or review it explicitly before updating.')
    if state.exists() and not previous and not args.adopt_existing_state:
        raise ValueError('Read and confirm the existing state/project, then use --adopt-existing-state.')
    if not state.exists() and any((workspace / name).exists() for name in
                                 ('ADVISOR_STATE_TEMPLATE.md', 'CONSULTOR_STATE_TEMPLATE.md')):
        raise ValueError('External template exists: initialize its state before setup; preserve the template.')
    for override in ('AGENTS.override.md', 'CLAUDE.local.md'):
        if (workspace / override).exists():
            raise ValueError(f'Review existing {override} before setup.')
    template = (ROOT / 'templates/AGENTS.md').read_text(encoding='utf-8')
    method = template.replace('{{STATE_FILE}}', args.state_file).encode('utf-8')
    wanted = {'AGENTS.md': method}
    if args.harness == 'claude':
        wanted['CLAUDE.md'] = b'# Project Advisor workspace\n\n@AGENTS.md\n'
    if previous and set(previous['files']) != set(wanted):
        raise ValueError('Unexpected managed files. Review the manifest before updating.')
    snapshots = {}
    for name, data in wanted.items():
        path = workspace / name
        if path.is_symlink():
            raise ValueError(f'Refusing symlink: {name}')
        old = path.read_bytes() if path.exists() else None
        snapshots[name] = old
        if previous:
            if old is None or digest(old) != previous['files'][name]:
                raise ValueError(f'Local edits in {name}. Merge manually; keep custom rules in ADVISOR_LOCAL.md.')
        elif old is not None:
            raise ValueError(f'Existing unmanaged {name}; review it before setup.')
        if old != data:
            print(''.join(difflib.unified_diff(
                (old or b'').decode('utf-8').splitlines(True),
                data.decode('utf-8').splitlines(True), fromfile=f'{name} (current)', tofile=f'{name} (proposed)')))
    if args.harness != 'claude' and (workspace / 'CLAUDE.md').exists():
        raise ValueError('Existing CLAUDE.md requires review; no adapter will be overwritten.')
    manifest = {'schema': 1, 'method_version': VERSION, 'project': str(project),
                'harness': args.harness, 'state_file': args.state_file,
                'files': {name: digest(data) for name, data in wanted.items()}}
    state_before = state.read_bytes() if state.exists() else None
    manifest_before = manifest_path.read_bytes() if manifest_path.exists() else None
    print(f'Workspace: {workspace}\nProject: {project}\nState: {args.state_file} (preserved if present)')
    if not args.apply:
        print('Preview only. Review the diff; use --apply to write.')
        return
    workspace.mkdir(parents=True, exist_ok=True)
    lock = workspace / '.advisor-setup.lock'
    with lock.open('x', encoding='utf-8') as stream:
        stream.write(str(os.getpid()))
    try:
        for name, old in snapshots.items():
            path = workspace / name
            if (path.read_bytes() if path.exists() else None) != old:
                raise ValueError(f'Concurrent change in {name}; retry after review.')
        if (state.read_bytes() if state.exists() else None) != state_before:
            raise ValueError('State changed during setup; retry after review.')
        if (manifest_path.read_bytes() if manifest_path.exists() else None) != manifest_before:
            raise ValueError('Manifest changed during setup; retry after review.')
        # Instruction files are replaced atomically; manifest is committed last.
        for name, data in wanted.items():
            if snapshots[name] != data:
                atomic_write(workspace / name, data)
        if state_before is None:
            initial = ('# Advisor state\n\n## Project\n\n' + str(project) +
                       '\n\n## Current objective\n\nNot defined.\n\n## Active decisions\n\nNone recorded.\n\n'
                       '## Latest worker task and result\n\nNot defined.\n\n## Open issues\n\nNot defined.\n\n'
                       '## Next step\n\nAsk for the project objective.\n')
            with state.open('x', encoding='utf-8', newline='\n') as stream:
                stream.write(initial)
        atomic_write(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    finally:
        lock.unlink()
    print('Workspace prepared. Existing state was not rewritten. Verify loading in a fresh session.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--harness', choices=('codex', 'claude', 'opencode'), required=True)
    parser.add_argument('--state-file', default='ADVISOR_STATE.md')
    parser.add_argument('--adopt-existing-state', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        prepare(args)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
