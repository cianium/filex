<div align="center">

# FileX

**A lightweight Python file organizer for Android shared storage through Termux**

**Extension-based sorting · SHA-256 duplicate detection · Project-folder exclusions**

![Status](https://img.shields.io/badge/Status-Experimental-f59e0b)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab)
![Releases](https://img.shields.io/badge/Releases-None-64748b)

[Source Code](https://github.com/cianium/filex) · [Safe Usage Guide](docs/SAFE_USAGE.md)

</div>

> **Important — this script moves real files immediately.** There is **no dry-run, confirmation prompt, rollback, or undo**. Do not run it on valuable or irreplaceable files. Always use a separate backup and test on a disposable directory first.

## Overview

FileX is an experimental Python script for sorting files in **Termux-accessible Android shared storage**. It scans recursively, skips common development directories and project trees, groups files by extension, and separates exact-content duplicates detected within the same run.

The current implementation uses Python's standard library only. It is **not** a general-purpose storage manager, synchronization service or backup utility.

## Current features

| Feature | Implementation |
| :-- | :-- |
| **Recursive file discovery** | Scans `~/storage/shared` |
| **Sorting by extension** | Moves files to `Organized/<lowercase-extension>/` |
| **No-extension files** | Moves files to `Organized/NoExtension/` |
| **Duplicate detection** | Compares SHA-256 file content within the current scan |
| **Duplicate separation** | Moves later duplicate files into `Organized/Duplicates/`; it does **not** delete them |
| **Project protection** | Skips paths containing `Android`, `Organized`, `.git`, `node_modules`, `venv`, or `__pycache__`, and detects common project marker files |
| **Name collisions** | Adds numeric suffixes when an output filename already exists |

### Example destination layout

```text
~/storage/shared/
└── Organized/
    ├── jpg/
    ├── pdf/
    ├── mp3/
    ├── NoExtension/
    └── Duplicates/
```

This diagram illustrates destination folder names; the script creates only folders needed for the scanned file types, plus the main output and duplicates folders.

## Requirements

- **Python 3.8+** (the source uses the assignment-expression / walrus operator).
- **Termux** and permission to access the shared-storage path.
- A **separate backup** or expendable test dataset.

There are no third-party Python package dependencies and currently no argument parser.

## Safer evaluation

1. **Back up** important data separately.
2. Prepare a **disposable test directory** containing sample files and a sample coding project.
3. Inspect [`main.py`](main.py) and temporarily change its `ROOT` constant from `Path.home() / "storage" / "shared"` to the disposable test directory.
4. Check all expected source/destination locations before running:
   ```bash
   python main.py
   ```
5. Verify the output directories and compare the test dataset with your backup.

**Do not use this command directly with the default shared-storage path until you are certain about its effects.** Read the complete [safe-usage checklist](docs/SAFE_USAGE.md).

## Implementation notes

```text
filex/
├── main.py              Recursive scan, SHA-256 hashing and file moves
├── docs/
│   └── SAFE_USAGE.md   Precautions and planned safeguards
├── .gitignore
└── README.md
```

The program uses `pathlib`, `hashlib` and `shutil`. It calls `shutil.move()` to relocate files, so it **changes their original paths**. Hashing a file is not a backup or data integrity guarantee for the destination.

## Known limitations

- **No `--dry-run` or `--apply` distinction:** `python main.py` performs changes immediately.
- **No undo, operation journal or manifest.**
- **No configurable CLI source/destination:** the shared-storage root is currently hard-coded.
- **No comprehensive symlink/path containment checks:** do not assume symlinked files are safely excluded.
- **Silent exceptions:** failed hashes or moves can be skipped without a structured error report.
- **Per-run duplicate detection only:** no durable content index or reconciliation between executions.
- **No automated unit tests, CI workflow or independently verified Android compatibility matrix.**

## Development priorities

1. Default to a **read-only `--dry-run`**, requiring an explicit `--apply` to move files.
2. Add configurable roots with path/symlink validation and testable exclusions.
3. Add a per-file operation journal, meaningful error messages, and a recovery plan.
4. Test duplicate classification, permission errors, name collisions and interrupted moves.
5. Create a repeatable test suite before distributing a first stable release.

## Releases

There are currently **no GitHub Releases and no version tags**. The repository's `main` branch is an **experimental script**, not a verified stable release.

A versioned `v1.0.0` should be published only after dry-run protections, test coverage and recovery behavior are implemented and reviewed. No live demo or project website is available at present.

## License

There is currently **no repository-wide `LICENSE` file**. Public source visibility does not grant a right to copy, redistribute or commercially relicense the project. Ask the maintainer before reuse.

---

<div align="center">

**FileX — organize carefully, verify before moving.**

</div>
