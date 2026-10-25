# FileX — safe-usage guide

## Read before running

The current `main.py` scans the shared storage root `~/storage/shared` and calls `shutil.move()`. It **changes file locations**, including moving duplicates into a folder called `Organized/Duplicates`.

There is **no dry-run switch, undo function or reliable audit trail**. Do not run it on the only copy of valuable data.

## Safe verification procedure

1. Make a separate backup of any important files.
2. Copy sample files and a sample project into a disposable directory.
3. Review the Python `ROOT` variable and redirect it to **that test directory** before executing.
4. Confirm which files were moved and where; test duplicates, repeated filenames and project exclusions.
5. Stop using the tool if files are unexpectedly classified or permissions fail.
6. Re-run only on a verified copy until dry-run and undo are implemented.

## Requirements for safe future automation

- `--dry-run` as a default; `--apply` for explicit modifications.
- Configurable, validated source/destination directory.
- Symlink and path containment checks.
- Deterministic plan with per-file hashes, conflict policy, move journal and recovery guidance.
- Tests for access errors, interrupted moves, duplicate runs and idempotency.
- Structured error logging (avoid silent exception swallowing).

These are a **roadmap**, not implemented features.
