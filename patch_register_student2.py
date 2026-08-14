import unicodedata

FILE = "app/templates/auth/register_student.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Them nut "Dang ky bang Google" (them thanh chia "Hoac" + nut, ngay
#    sau nut "Dang ky" thuong, truoc khi dong the </form>)
old_submit_block = '''<div class="pt-stack-md">
<button class="w-full bg-primary-container text-white py-stack-md px-stack-lg rounded-2xl font-semibold text-lg hover:opacity-90 active:opacity-80 transition-all shadow-md shadow-primary-container/20" type="submit">
                                Đăng ký
                            </button>
</div>
</form>'''
assert content.count(old_submit_block) == 1, "Khong tim thay nut Dang ky / </form>."

new_submit_block = '''<div class="pt-stack-md">
<button class="w-full bg-primary-container text-white py-stack-md px-stack-lg rounded-2xl font-semibold text-lg hover:opacity-90 active:opacity-80 transition-all shadow-md shadow-primary-container/20" type="submit">
                                Đăng ký
                            </button>
</div>
<div class="flex items-center gap-4 py-2">
<div class="h-px bg-outline-variant flex-1"></div>
<span class="text-xs font-semibold text-secondary uppercase tracking-wider">Hoặc</span>
<div class="h-px bg-outline-variant flex-1"></div>
</div>
<button id="google-register-btn" type="button" class="w-full flex items-center justify-center gap-3 border border-outline-variant bg-surface-container-lowest py-stack-md px-stack-lg rounded-2xl font-semibold hover:bg-surface-container-low active:scale-[0.98] transition-all">
<svg class="w-5 h-5" viewbox="0 0 24 24">
<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"></path>
<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
</svg>
<span>Đăng ký bằng Google</span>
</button>
</form>'''
content = content.replace(old_submit_block, new_submit_block)

# 2. Them script goi Supabase OAuth (dung chung 1 luong voi trang login:
#    signInWithOAuth -> redirect /auth/callback -> POST /auth/set-session
#    -> /chat). Chen truoc </body>.
old_end = '</body></html>'
assert content.count(old_end) == 1, "Khong tim thay </body></html>."
new_end = '''<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script>
    (function () {
        var supabaseClient = window.supabase.createClient(
            "{{ supabase_url }}",
            "{{ supabase_anon_key }}"
        );
        var btn = document.getElementById('google-register-btn');
        if (btn) {
            btn.addEventListener('click', async function () {
                var result = await supabaseClient.auth.signInWithOAuth({
                    provider: 'google',
                    options: {
                        redirectTo: window.location.origin + '/auth/callback'
                    }
                });
                if (result.error) {
                    alert('Không thể đăng ký bằng Google: ' + result.error.message);
                }
            });
        }
    })();
</script>
</body></html>'''
content = content.replace(old_end, new_end)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
