import unicodedata

FILE = "app/core/lop_config.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

old_block = '''DANH_SACH_LOP = {
    "10": [
        "C1A", "C1B", "C2A", "C2B", "C3A", "C3B",
        "C4", "C5A", "C5B", "C6", "C7", "C8", "C9",
    ],
    "11": [
        "C1A", "C1B", "C2A", "C2B", "C3A", "C3B",
        "C4", "C5A", "C5B", "C6", "C7", "C8", "C9",
    ],
}'''

assert content.count(old_block) == 1, "Khong tim thay DANH_SACH_LOP cu."

new_block = '''DANH_SACH_LOP = {
    "10": [
        "C1A", "C1B", "C2A", "C2B", "C3A", "C3B",
        "C4", "C5A", "C5B", "C6", "C7", "C8", "C9",
        "Tự do",
    ],
    "11": [
        "C1A", "C1B", "C2A", "C2B", "C3A", "C3B",
        "C4", "C5A", "C5B", "C6", "C7", "C8", "C9",
        "Tự do",
    ],
}

# Ma lop that tren Google Classroom (course ID), giai ma tu link Classroom
# giao vien cung cap (https://classroom.google.com/c/<base64 cua ID>).
# Chua dung ngay, chuan bi san cho buoc dong bo danh sach email hoc sinh
# (doi chieu email tu dong khi hoc sinh dang ky/dang nhap) o phien ban sau.
MA_LOP_CLASSROOM = {
    ("10", "C1A"): "874604932932",
    ("10", "C1B"): "869140904250",
    ("10", "C2A"): "869140895807",
    ("10", "C2B"): "874605698192",
    ("10", "C3A"): "874600387523",
    ("10", "C3B"): "874605505765",
    ("10", "C4"): "874600557196",
    ("10", "C5A"): "874604891604",
    ("10", "C5B"): "869140911962",
    ("10", "C6"): "874605633509",
    ("10", "C7"): "874605018881",
    ("10", "C8"): "874605552252",
    ("10", "C9"): "869140892877",
    ("10", "Tự do"): "874602361962",
    ("11", "C1A"): "874605178602",
    ("11", "C1B"): "874604954652",
    ("11", "C2A"): "869140892894",
    ("11", "C2B"): "869140629699",
    ("11", "C3A"): "874606260155",
    ("11", "C3B"): "874605178618",
    ("11", "C4"): "874606089536",
    ("11", "C5A"): "874605473964",
    ("11", "C5B"): "874605494341",
    ("11", "C6"): "874604997269",
    ("11", "C7"): "874600557261",
    ("11", "C8"): "869140897300",
    ("11", "C9"): "874605025088",
    ("11", "Tự do"): "855865997421",
}'''

content = content.replace(old_block, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
