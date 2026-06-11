from pathlib import Path
import shutil
import hashlib

ROOT = Path.home() / "storage" / "shared"

OUTPUT = ROOT / "Organized"
DUPLICATES = OUTPUT / "Duplicates"

IGNORE_DIRS = {
    "Android",
    "Organized",
    ".git",
    "node_modules",
    "venv",
    "__pycache__"
}

PROJECT_MARKERS = {
    ".git",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "Cargo.toml",
    "composer.json",
    "pom.xml",
    "build.gradle"
}


def file_hash(path):
    sha = hashlib.sha256()

    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                sha.update(chunk)

        return sha.hexdigest()

    except Exception:
        return None


def inside_project(file):
    current = file.parent

    while current != ROOT:

        for marker in PROJECT_MARKERS:
            if (current / marker).exists():
                return True

        current = current.parent

    return False


def scan_files():
    files = []

    for file in ROOT.rglob("*"):

        if not file.is_file():
            continue

        if any(part in IGNORE_DIRS for part in file.parts):
            continue

        if inside_project(file):
            continue

        files.append(file)

    return files


def safe_name(path):
    counter = 1
    new_path = path

    while new_path.exists():

        new_path = (
            path.parent /
            f"{path.stem}_{counter}{path.suffix}"
        )

        counter += 1

    return new_path


def organize():

    OUTPUT.mkdir(exist_ok=True)
    DUPLICATES.mkdir(exist_ok=True)

    hashes = {}

    moved = 0
    duplicates = 0

    files = scan_files()

    print("Files found:", len(files))

    for file in files:

        ext = file.suffix.lower()

        if ext == "":
            folder = OUTPUT / "NoExtension"
        else:
            folder = OUTPUT / ext[1:]

        folder.mkdir(parents=True, exist_ok=True)

        current_hash = file_hash(file)

        if current_hash:

            if current_hash in hashes:

                dup_target = safe_name(
                    DUPLICATES / file.name
                )

                try:
                    shutil.move(
                        str(file),
                        str(dup_target)
                    )

                    duplicates += 1

                except Exception:
                    pass

                continue

            hashes[current_hash] = file

        target = safe_name(
            folder / file.name
        )

        try:

            shutil.move(
                str(file),
                str(target)
            )

            moved += 1

        except Exception:
            pass

    print("\n===== DONE =====")
    print("Moved:", moved)
    print("Duplicates:", duplicates)


if __name__ == "__main__":
    organize()
