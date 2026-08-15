import unicodedata

FILE = "app/templates/index.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# ---- 1) Nut o header: "Dang nhap" -> tuy trang thai dang nhap ----
old_header = '''<div class="flex items-center gap-4">
<button
    onclick="window.location.href='/login'"
    class="px-6 py-2 bg-primary text-on-primary rounded-lg font-label-md btn-shadow active:scale-95 duration-150">
    Đăng nhập
</button>
</div>'''

assert content.count(old_header) == 1, "Khong tim thay nut Dang nhap o header."

new_header = '''<div class="flex items-center gap-4">
{% if da_dang_nhap %}
<span class="hidden md:inline font-body-md text-body-md text-on-surface-variant">Xin chào, {{ user_display_name }}</span>
<button
    onclick="window.location.href='/chat'"
    class="px-6 py-2 bg-primary text-on-primary rounded-lg font-label-md btn-shadow active:scale-95 duration-150">
    Vào Chat
</button>
{% else %}
<button
    onclick="window.location.href='/login'"
    class="px-6 py-2 bg-primary text-on-primary rounded-lg font-label-md btn-shadow active:scale-95 duration-150">
    Đăng nhập
</button>
{% endif %}
</div>'''

content = content.replace(old_header, new_header)

# ---- 2) Nut CTA lon o Hero: "Dang nhap ngay" -> tuy trang thai dang nhap ----
old_hero = '''<div class="flex flex-col sm:flex-row gap-4 justify-center">
<button
    onclick="window.location.href='/login'"
    class="px-8 py-4 bg-primary text-on-primary rounded-xl font-label-md btn-shadow text-lg">
    Đăng nhập ngay
</button>
<a href="#gioi-thieu" class="px-8 py-4 bg-surface-container-low text-primary border border-outline-variant/30 rounded-xl font-label-md hover:bg-surface-container-high transition-all text-lg inline-block text-center">Giới thiệu chi tiết</a>
</div>'''

assert content.count(old_hero) == 1, "Khong tim thay nut CTA Dang nhap ngay o Hero."

new_hero = '''<div class="flex flex-col sm:flex-row gap-4 justify-center">
{% if da_dang_nhap %}
<button
    onclick="window.location.href='/chat'"
    class="px-8 py-4 bg-primary text-on-primary rounded-xl font-label-md btn-shadow text-lg">
    Vào Chat
</button>
{% else %}
<button
    onclick="window.location.href='/login'"
    class="px-8 py-4 bg-primary text-on-primary rounded-xl font-label-md btn-shadow text-lg">
    Đăng nhập ngay
</button>
{% endif %}
<a href="#gioi-thieu" class="px-8 py-4 bg-surface-container-low text-primary border border-outline-variant/30 rounded-xl font-label-md hover:bg-surface-container-high transition-all text-lg inline-block text-center">Giới thiệu chi tiết</a>
</div>'''

content = content.replace(old_hero, new_hero)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
