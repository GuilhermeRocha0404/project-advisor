"""Prepare one advisor workspace. Preview first; never overwrite project state."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.1.3'
MANIFEST = '.advisor-workspace.json'
STATE_NAMES = ('ADVISOR_STATE.md', 'CONSULTOR_STATE.md')
RECOVERY_GUIDANCE = (
    ' If setup was interrupted or the manifest is missing, preserve all files and recover a trusted '
    'manifest backup if available. Otherwise confirm the target project and inspect the state for '
    'incomplete content. Compare unmanaged AGENTS.md/CLAUDE.md with the intended package files; '
    'move only confirmed orphaned instruction files to a backup outside the workspace. '
    'Then preview with --adopt-existing-state and the matching --state-file before using --apply. '
    'Do not delete state or discard custom instructions. '
    'See references/HARNESSES.md#interrupted-first-install.'
)


def read_manifest(path):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if (not isinstance(data, dict) or data.get('schema') != 1
                or not isinstance(data.get('project'), str)
                or not Path(data['project']).is_absolute()
                or data.get('state_file') not in STATE_NAMES
                or data.get('harness') not in ('codex', 'claude', 'opencode')
                or not isinstance(data.get('files'), dict)
                or not all(isinstance(k, str) and isinstance(v, str)
                           for k, v in data['files'].items())):
            raise ValueError('Invalid manifest structure.')
        return data
    except (ValueError, UnicodeError) as error:
        raise ValueError('Invalid workspace manifest. Preserve state and instructions; '
                         'recover the binding from a trusted backup or review it explicitly. '
                         'Do not delete the manifest to force setup.') from error


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
    if workspace == ROOT or ROOT in workspace.parents or workspace in ROOT.parents:
        raise ValueError('Advisor and installed skill must have separate directory trees.')
    manifest_path = workspace / MANIFEST
    if manifest_path.is_symlink():
        raise ValueError('Manifest cannot be a symlink.')
    previous = read_manifest(manifest_path) if manifest_path.exists() else None
    args.state_file = args.state_file or (previous['state_file'] if previous else 'ADVISOR_STATE.md')
    if args.state_file not in STATE_NAMES:
        raise ValueError('Unsupported state filename.')
    if previous:
        if Path(previous['project']).resolve() != project:
            raise ValueError('Project binding differs. Use another workspace for another project. '
                             'For a moved checkout, verify its identity and explicitly review '
                             'the manifest project path; setup never rebinds automatically.')
        if previous['state_file'] != args.state_file:
            raise ValueError('Preserve the existing state filename.')
        if previous['harness'] != args.harness:
            raise ValueError('Harness change requires manual review of existing adapters.')
    state = workspace / args.state_file
    other = workspace / ('CONSULTOR_STATE.md' if args.state_file == 'ADVISOR_STATE.md' else 'ADVISOR_STATE.md')
    if other.exists() or other.is_symlink():
        raise ValueError('Another state exists. Resolve it explicitly; do not create competing states.')
    if state.is_symlink():
        raise ValueError('State cannot be a symlink.')
    if previous and not state.exists():
        raise ValueError('Existing workspace state is missing. Recover or review it explicitly before updating.')
    if state.exists() and not previous and not args.adopt_existing_state:
        raise ValueError('Read and confirm the existing state/project, then use --adopt-existing-state.'
                         + RECOVERY_GUIDANCE)
    if not state.exists() and any((workspace / name).exists() for name in
                                 ('ADVISOR_STATE_TEMPLATE.md', 'CONSULTOR_STATE_TEMPLATE.md')):
        raise ValueError('External template exists: initialize its state before setup; preserve the template.')
    for override in ('AGENTS.override.md', 'CLAUDE.local.md'):
        override_path = workspace / override
        if override_path.exists() or override_path.is_symlink():
            raise ValueError(f'Review existing {override} before setup.')
    # Universal newline reading intentionally produces UTF-8/LF on every platform.
    template = (ROOT / 'templates/AGENTS.md').read_text(encoding='utf-8')
    method = template.replace('{{STATE_FILE}}', args.state_file).encode('utf-8')
    initial = (ROOT / 'references/STATE_SCHEMA.md').read_text(encoding='utf-8')
    initial = initial.replace('{{PROJECT_NAME}}', project.name)
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
            raise ValueError(f'Existing unmanaged {name}; review it before setup.' + RECOVERY_GUIDANCE)
        if old != data:
            print(''.join(difflib.unified_diff(
                (old or b'').decode('utf-8').splitlines(True),
                data.decode('utf-8').splitlines(True), fromfile=f'{name} (current)', tofile=f'{name} (proposed)')))
    claude_path = workspace / 'CLAUDE.md'
    if args.harness != 'claude' and (claude_path.exists() or claude_path.is_symlink()):
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
    try:
        with lock.open('x', encoding='utf-8') as stream:
            stream.write(str(os.getpid()))
    except FileExistsError as error:
        raise ValueError('Setup lock exists. Check its PID and whether another setup is active. '
                         'If it is confirmed stale, inspect interrupted writes and remove only '
                         '.advisor-setup.lock before retrying. No automatic removal was performed.') from error
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
            fd = os.open(state, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
                stream.write(initial)
        atomic_write(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    finally:
        lock.unlink()
    print('Workspace prepared. Existing state was not rewritten. Verify loading in a fresh session.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=f'Project Advisor method {VERSION}')
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--harness', choices=('codex', 'claude', 'opencode'), required=True)
    parser.add_argument('--state-file', choices=STATE_NAMES,
                        help='Defaults to the existing manifest name, or ADVISOR_STATE.md on first setup.')
    parser.add_argument('--adopt-existing-state', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        prepare(args)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
