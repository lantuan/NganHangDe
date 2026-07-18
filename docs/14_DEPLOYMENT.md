# DEPLOYMENT

Version: 1.0

Trạng thái

🟡 Đang triển khai

---

# Mục tiêu

Chuẩn hóa toàn bộ quá trình triển khai hệ thống.

Mọi môi trường (Local, VPS, Production) phải có cùng kiến trúc.

---

# Kiến trúc triển khai

Developer

↓

GitHub

↓

VPS

↓

FastAPI

↓

n8n

↓

Python

↓

Supabase

---

# Repository

GitHub

↓

main

↓

Production

---

# Branch

main

Production

---

dev

Phát triển

(TODO)

---

# Local

Máy phát triển.

Sử dụng

- VS Code
- Python
- Git
- Browser

---

# GitHub

Lưu

- Source Code
- JSON
- Python Generator
- Docs
- Templates

Không lưu

- PDF
- File tạm
- Cache
- Upload

---

# VPS

Chạy

- FastAPI
- n8n
- Python
- TeX Live
- Nginx

---

# FastAPI

Port

8000

---

# n8n

Port

5678

---

# Supabase

Cloud Database.

---

# Python

Virtual Environment

```
.venv
```

---

# TeX Live

Sinh PDF.

---

# systemd

Quản lý

FastAPI.

---

# Nginx

Reverse Proxy.

(TODO)

---

# Domain

(TODO)

---

# SSL

Let's Encrypt.

(TODO)

---

# Environment

.env

Không đưa lên GitHub.

---

# Upload

uploads/

Không đưa lên GitHub.

---

# Export

exports/

Không đưa lên GitHub.

---

# Temp

temp/

Không đưa lên GitHub.

---

# Logging

logs/

---

# Quy trình Deploy

Developer

↓

Git Commit

↓

Git Push

↓

GitHub

↓

VPS

↓

Git Pull

↓

Restart Service

↓

Kiểm tra

↓

Hoàn thành

---

# Quy trình Update

Developer

↓

Sửa Code

↓

Commit

↓

Push

↓

GitHub

↓

VPS Pull

↓

Restart

↓

Test

---

# Backup

Database

(TODO)

---

# Restore

(TODO)

---

# Monitoring

FastAPI

systemd

n8n

(TODO)

---

# Error Log

FastAPI

↓

systemctl

↓

journalctl

---

# Cấu trúc Production

GitHub

↓

FastAPI

↓

n8n

↓

Python

↓

TeX Live

↓

Supabase

---

# Danh sách Service

## FastAPI

nganhangde.service

---

## n8n

n8n.service

(TODO)

---

## Nginx

nginx.service

(TODO)

---

# Kiểm tra sau Deploy

□ FastAPI chạy.

□ n8n chạy.

□ API hoạt động.

□ Chat AI hoạt động.

□ Sinh đề hoạt động.

□ Python Generator hoạt động.

□ LaTeX hoạt động.

□ PDF sinh thành công.

□ Database kết nối.

□ Upload hoạt động.

□ Download hoạt động.

---

# Không Deploy

- File tạm.
- Cache.
- Upload.
- PDF.
- Log cũ.

---

# TODO

Docker.

Docker Compose.

CI/CD.

GitHub Actions.

Auto Deploy.

Auto Backup.

Multi Server.

Load Balancer.

Redis.

Celery.

Object Storage.

CDN.