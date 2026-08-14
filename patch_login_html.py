"""
Patch app/templates/auth/login.html:
1. Xoa 4 link nav placeholder (Tinh nang/Giai phap/Bang gia/Tai lieu) khong dan di dau.
2. Checkbox "Ghi nho dang nhap" -> co name=remember de gui len server.
3. Nut Google -> them id de gan JS that.
4. Them script Supabase JS (CDN) + logic goi signInWithOAuth khi bam nut Google.

Chay tren May (thu muc goc repo):
    cd ~/duong_dan_toi/NganHangDe
    python3 patch_login_html.py
"""

import unicodedata

FILE = "app/templates/auth/login.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Chuan hoa Unicode ve dang NFC truoc khi so khop chuoi: file HTML nay co
# the da duoc tao/luu tren macOS o dang NFD (dau tieng Viet tach roi khoi
# ky tu goc), trong khi chuoi can tim trong script nay o dang NFC -> neu
# khong chuan hoa se bao "khong tim thay" dù nhin bang mat giong het nhau.
content = unicodedata.normalize("NFC", content)

goc = len(content)

# ------------------------------------------------------
# 1. Xoa 4 link nav placeholder, giu logo + Dang ky
# ------------------------------------------------------
old_nav = '''<div class="hidden md:flex gap-gutter items-center">
<a class="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Tính năng</a>
<a class="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Giải pháp</a>
<a class="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Bảng giá</a>
<a class="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Tài liệu</a>
<a
    href="/register"
    class="bg-primary-container text-on-primary-container px-6 py-2 rounded-full font-label-md text-label-md hover:scale-105 active:scale-95 transition-transform inline-block"
>
    Đăng ký
</a>
</div>'''

new_nav = '''<div class="hidden md:flex gap-gutter items-center">
<a
    href="/register"
    class="bg-primary-container text-on-primary-container px-6 py-2 rounded-full font-label-md text-label-md hover:scale-105 active:scale-95 transition-transform inline-block"
>
    Đăng ký
</a>
</div>'''

assert content.count(old_nav) == 1, "Khong tim thay khoi nav can xoa (hoac bi trung)."
content = content.replace(old_nav, new_nav)

# ------------------------------------------------------
# 2. Checkbox "Ghi nho dang nhap" -> them name=remember
# ------------------------------------------------------
old_remember = '<input class="w-5 h-5 rounded border-outline text-primary focus:ring-primary cursor-pointer" type="checkbox"/>'
new_remember = '<input class="w-5 h-5 rounded border-outline text-primary focus:ring-primary cursor-pointer" type="checkbox" id="remember" name="remember" value="true"/>'

assert content.count(old_remember) == 1, "Khong tim thay checkbox Ghi nho dang nhap."
content = content.replace(old_remember, new_remember)

# ------------------------------------------------------
# 3. Nut Google -> them id="google-login-btn"
# ------------------------------------------------------
old_google_btn = '<button class="w-full h-14 border border-outline-variant bg-white flex items-center justify-center gap-3 rounded-[16px] hover:bg-surface-container-low active:scale-[0.98] transition-all duration-200" type="button">'
new_google_btn = '<button id="google-login-btn" class="w-full h-14 border border-outline-variant bg-white flex items-center justify-center gap-3 rounded-[16px] hover:bg-surface-container-low active:scale-[0.98] transition-all duration-200" type="button">'

assert content.count(old_google_btn) == 1, "Khong tim thay nut Google."
content = content.replace(old_google_btn, new_google_btn)

# ------------------------------------------------------
# 4. Them Supabase JS + logic dang nhap Google, truoc </body>
# ------------------------------------------------------
old_tail = "</body></html>"
assert content.count(old_tail) == 1, "Khong tim thay the dong </body></html>."

google_script = '''<!-- Dang nhap Google qua Supabase (client-side OAuth) -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script>
    (function () {
        var supabaseClient = window.supabase.createClient(
            "{{ supabase_url }}",
            "{{ supabase_anon_key }}"
        );
        var btn = document.getElementById('google-login-btn');
        if (btn) {
            btn.addEventListener('click', async function () {
                var result = await supabaseClient.auth.signInWithOAuth({
                    provider: 'google',
                    options: {
                        redirectTo: window.location.origin + '/auth/callback'
                    }
                });
                if (result.error) {
                    alert('Không thể đăng nhập bằng Google: ' + result.error.message);
                }
            });
        }
    })();
</script>
</body></html>'''

content = content.replace(old_tail, google_script)

# ------------------------------------------------------
# Ghi file
# ------------------------------------------------------
with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
