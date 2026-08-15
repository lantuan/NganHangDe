import unicodedata

FILE = "app/templates/chat/chat.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

old_bottom = '''            <!-- Bottom -->
            <div class="border-t p-3 space-y-1">
                <button class="sidebar-link w-full flex items-center gap-3 rounded-xl px-4 py-3">
                    <span class="material-symbols-outlined">analytics</span>
                    Đánh giá học lực
                </button>
            </div>'''

assert content.count(old_bottom) == 1, "Khong tim thay khoi Bottom cua sidebar."

new_bottom = '''            <!-- Bottom -->
            <div class="border-t p-3 space-y-1">
                <button class="sidebar-link w-full flex items-center gap-3 rounded-xl px-4 py-3">
                    <span class="material-symbols-outlined">analytics</span>
                    Đánh giá học lực
                </button>
                <a href="/logout" class="sidebar-link w-full flex items-center gap-3 rounded-xl px-4 py-3" style="text-decoration:none;color:inherit;">
                    <span class="material-symbols-outlined">logout</span>
                    Đăng xuất
                </a>
            </div>'''

content = content.replace(old_bottom, new_bottom)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
