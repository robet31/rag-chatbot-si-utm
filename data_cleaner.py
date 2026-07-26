import re
import os
import glob

NAVIGATION_PATTERNS = [
    r"^Skip to content$",
    r"^Search for:$",
    r"^Search$",
    r"^Scroll to Top$",
    r"^Please enable JavaScript.*$",
    r"^Link$",
    r"^Kuisioner Akreditasi$",
    r"^Ristek Dikti$",
    r"^Universitas Trunojoyo Madura$",
    r"^Sistem Informasi$",
    r"^Informatika$",
    r"^Pos-pos Terbaru$",
    r"^Komentar Terbaru$",
    r"^Arsip$",
    r"^Kategori$",
    r"^Meta$",
    r"^Masuk$",
    r"^Entries RSS$",
    r"^Comments RSS$",
    r"^WordPress\.org$",
    r"^Scroll to Top$",
    r"^\.\.\.$",
    r"^0$",
    r"^\(\d+\)$",
]

SIDEBAR_KEYWORDS = [
    "kuisioner akreditasi", "ristek dikti", "universitas trunojoyo",
    "pos-pos terbaru", "komentar terbaru", "arsip", "kategori", "meta",
    "masuk", "entries rss", "comments rss", "wordpress.org",
    "scroll to top", "skip to content",
]

def is_navigation_line(line):
    stripped = line.strip()
    if not stripped:
        return True
    for pattern in NAVIGATION_PATTERNS:
        if re.match(pattern, stripped, re.IGNORECASE):
            return True
    return False

def is_sidebar_block(text):
    lower = text.lower()
    keyword_count = sum(1 for kw in SIDEBAR_KEYWORDS if kw in lower)
    return keyword_count >= 2

def clean_file(input_path, output_path=None):
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    clean_lines = []
    buffer = []
    in_sidebar = False

    for line in lines:
        stripped = line.strip()

        if is_navigation_line(line):
            continue

        if len(stripped) < 2:
            continue

        buffer.append(stripped)

        if len(buffer) >= 3:
            chunk = " | ".join(buffer[-3:])
            if is_sidebar_block(chunk):
                in_sidebar = True
                break

        clean_lines.append(line)

    if not output_path:
        output_path = input_path

    result = "".join(clean_lines)
    if result.strip():
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

    original_size = len("".join(lines))
    cleaned_size = len(result)
    saved = int((1 - cleaned_size / original_size) * 100) if original_size > 0 else 0
    return original_size, cleaned_size, saved

def clean_all(data_dir):
    txt_files = glob.glob(os.path.join(data_dir, "*.txt"))
    total_original = 0
    total_cleaned = 0

    print(f"Membersihkan {len(txt_files)} file .txt dari HTML artifacts...\n")
    for f in sorted(txt_files):
        orig, cleaned, pct = clean_file(f)
        total_original += orig
        total_cleaned += cleaned
        if pct > 5:
            print(f"  ⚡ {os.path.basename(f)}: hemat {pct}% ({orig//1000}k -> {cleaned//1000}k)")
        else:
            print(f"  ✅ {os.path.basename(f)}: bersih ({orig//1000}k)")

    total_saved = int((1 - total_cleaned / total_original) * 100) if total_original > 0 else 0
    print(f"\nSelesai! Total: {total_original//1000}KB -> {total_cleaned//1000}KB (hemat {total_saved}%)")

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "data"
    clean_all(data_dir)
