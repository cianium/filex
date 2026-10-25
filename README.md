# FileX — File Organizer for Termux

> **Status: working Python script / experimental. Operates on real files — back up your data before running.**

FileX recursively scans Android shared storage exposed in Termux, groups files by extension, detects exact-content duplicates within the current scan using SHA-256, and avoids directories that look like programming projects.

## Requirements

- Python 3 with access to Termux shared storage
- File storage permissions granted by the device owner

No third-party Python packages are required by the current script.

## How it works

- Scans `~/storage/shared`
- Skips `Android`, `Organized`, `.git`, `node_modules`, `venv` and `__pycache__`
- Skips project trees identified by marker files such as `package.json`, `.git` and `pyproject.toml`
- Moves files to `~/storage/shared/Organized/<extension>/`
- Moves duplicate files found **during the same scan** to `~/storage/shared/Organized/Duplicates/`
- Avoids overwrites by suffixing colliding filenames

## Run

```bash
python main.py
```

**Warning:** this command moves files immediately; there is currently **no dry-run, undo or interactive confirmation**. Test against an expendable backup only. Do not execute directly against important shared storage without reviewing and modifying the `ROOT` configuration.

## Known limitations

- Exceptions during file moves and hashing are not reported in a structured log.
- Duplicate detection is per run; it is not a persistent file index.
- A move across filesystems might copy and remove the original; this is not a backup system.
- No automated tests, CLI argument parsing or preview mode are currently included.

## Development roadmap

1. Add `--dry-run` as the default mode, with explicit `--apply` to move files.
2. Add a testable configurable source/destination and protection against path traversal/symlinks.
3. Add unit tests for project detection, duplicate handling and error recovery.
4. Add structured logs, an operation manifest and an optional undo workflow.

## License

No repository license is currently specified. Ask the maintainer before redistributing.
