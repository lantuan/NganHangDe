import unicodedata

FILE = "app/templates/chat/chat.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# Them dong "Khoi X - Lop Y" vao account-badge (duoi ten/email), chi
# hien khi co du lieu (hoc sinh da chon lop o /chon-lop).
old_badge = '''                    <div class="account-badge" title="{{ user_email | default('') }}">
                        <span class="material-symbols-outlined">account_circle</span>
                        <div class="account-badge-text">
                            <span class="account-badge-name">{{ user_display_name | default('') }}</span>
                            <span class="account-badge-email">{{ user_email | default('') }}</span>
                        </div>
                    </div>'''
assert content.count(old_badge) == 1, "Khong tim thay account-badge."

new_badge = '''                    <div class="account-badge" title="{{ user_email | default('') }}">
                        <span class="material-symbols-outlined">account_circle</span>
                        <div class="account-badge-text">
                            <span class="account-badge-name">{{ user_display_name | default('') }}</span>
                            <span class="account-badge-email">{{ user_email | default('') }}</span>
                            {% if user_khoi and user_lop %}
                            <span class="account-badge-email">Khối {{ user_khoi }} - {{ user_lop }}</span>
                            {% endif %}
                        </div>
                    </div>'''
content = content.replace(old_badge, new_badge)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
