import unicodedata

FILE = "app/templates/auth/teacher_coming_soon.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Loi gioi thieu di dom hon
old_intro = '<p class="font-body-lg text-body-lg text-on-surface-variant">Chức năng dành cho giáo viên đang được phát triển.</p>'
new_intro = '<p class="font-body-lg text-body-lg text-on-surface-variant">Đội ngũ đang cặm cụi "soạn giáo án" cho tính năng này — hứa ra mắt sớm, không để thầy cô đợi lâu như học sinh đợi tiếng trống hết giờ!</p>'
assert content.count(old_intro) == 1, "Khong tim thay doan gioi thieu."
content = content.replace(old_intro, new_intro)

# 2. Nut "Quay lai" -> ve dung trang /register thay vi link chet "#"
old_back = '<a class="w-full sm:w-auto px-stack-lg py-stack-md font-label-md text-label-md text-primary-container border border-primary-container rounded-xl hover:bg-surface-container transition-all flex items-center justify-center gap-stack-sm" href="#">'
new_back = '<a class="w-full sm:w-auto px-stack-lg py-stack-md font-label-md text-label-md text-primary-container border border-primary-container rounded-xl hover:bg-surface-container transition-all flex items-center justify-center gap-stack-sm" href="/register">'
assert content.count(old_back) == 1, "Khong tim thay nut Quay lai."
content = content.replace(old_back, new_back)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
