from pathlib import Path


OUTPUT_NAME = "source_dump.txt"
TARGET_EXTS = {".asm", ".inc"}


def collect_source_files(root: Path):
    files = [
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in TARGET_EXTS
    ]
    files.sort(key=lambda p: str(p.relative_to(root)).lower())
    return files


def read_text_with_fallback(path: Path) -> str:
    for enc in ("utf-8", "cp949", "euc-kr", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            pass
    return "[ERROR] Could not decode file."


def main():
    root = Path(__file__).resolve().parent
    output_path = root / OUTPUT_NAME
    files = collect_source_files(root)

    lines = []
    lines.append(f"ROOT: {root}")
    lines.append(f"TOTAL FILES: {len(files)}")
    lines.append("=" * 80)
    lines.append("")

    for i, file_path in enumerate(files, start=1):
        rel = file_path.relative_to(root)

        lines.append("=" * 80)
        lines.append(f"[FILE {i}/{len(files)}] {rel}")
        lines.append("-" * 80)
        lines.append(f"--- BEGIN FILE: {rel} ---")
        lines.append("")

        content = read_text_with_fallback(file_path)
        lines.append(content.rstrip())

        lines.append("")
        lines.append(f"--- END FILE: {rel} ---")
        lines.append("=" * 80)
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()