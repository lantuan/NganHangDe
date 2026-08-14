import unicodedata

FILE = "app/templates/chat/chat.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Font-size cua button/input/textarea dang bi trinh duyet mac dinh
#    (nho hon text thuong) vi CSS chi reset font-family, khong reset
#    font-size. Sua de dong bo voi cac trang khac (Tailwind text-base/lg).
old_font = '''        button, input, textarea { font-family: inherit; }'''
assert content.count(old_font) == 1, "Khong tim thay dong reset font button/input/textarea."

new_font = '''        button, input, textarea { font-family: inherit; font-size: 16px; }

        #new-chat-btn,
        #send-btn { font-size: 18px; }

        .account-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 14px;
            border-radius: 12px;
            background: #f1f5f9;
            max-width: 240px;
        }

        .account-badge .material-symbols-outlined {
            font-size: 22px;
            color: var(--color-primary);
        }

        .account-badge-text {
            display: flex;
            flex-direction: column;
            line-height: 1.25;
            overflow: hidden;
        }

        .account-badge-name {
            font-size: 13px;
            font-weight: 600;
            color: #0f172a;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .account-badge-email {
            font-size: 11px;
            color: var(--color-slate-500);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }'''

content = content.replace(old_font, new_font)

# 2. Logo goc trai (sidebar) chua bam duoc, bien thanh <a href="/">
old_logo = '''            <div class="p-6 border-b">
                <div class="flex items-center gap-3">
                    <div class="w-11 h-11 rounded-xl bg-primary text-white flex items-center justify-center">
                        <span class="material-symbols-outlined">auto_awesome</span>
                    </div>
                    <div>
                        <h1 class="font-bold text-xl" style="margin:0;">Ngân Hàng Đề AI</h1>
                        <p class="text-xs text-slate-500" style="margin:0;">Teacher Assistant</p>
                    </div>
                </div>
            </div>'''
assert content.count(old_logo) == 1, "Khong tim thay khoi logo sidebar."

new_logo = '''            <div class="p-6 border-b">
                <a href="/" class="flex items-center gap-3" style="text-decoration:none;color:inherit;" title="Về trang chủ">
                    <div class="w-11 h-11 rounded-xl bg-primary text-white flex items-center justify-center">
                        <span class="material-symbols-outlined">auto_awesome</span>
                    </div>
                    <div>
                        <h1 class="font-bold text-xl" style="margin:0;">Ngân Hàng Đề AI</h1>
                        <p class="text-xs text-slate-500" style="margin:0;">Teacher Assistant</p>
                    </div>
                </a>
            </div>'''
content = content.replace(old_logo, new_logo)

# 3. Bo nut Home ben phai header, thay bang badge ten/email tai khoan
old_home = '''                <div class="flex items-center gap-2">
                    <a href="/" class="icon-btn w-10 h-10 rounded-xl flex items-center justify-center" title="Ve trang chu">
                        <span class="material-symbols-outlined">home</span>
                    </a>
                </div>'''
assert content.count(old_home) == 1, "Khong tim thay nut Home o header."

new_home = '''                <div class="flex items-center gap-2">
                    <div class="account-badge" title="{{ user_email | default('') }}">
                        <span class="material-symbols-outlined">account_circle</span>
                        <div class="account-badge-text">
                            <span class="account-badge-name">{{ user_display_name | default('') }}</span>
                            <span class="account-badge-email">{{ user_email | default('') }}</span>
                        </div>
                    </div>
                </div>'''
content = content.replace(old_home, new_home)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
