/*
 * SERVICE WORKER - Ngân Hàng Đề AI cài như ứng dụng (PWA), cô Lan 28/10/2026.
 * Phục vụ ở /sw.js (app/main.py) để phạm vi là cả trang web.
 *
 * Nguyên tắc AN TOÀN (không làm hỏng web đang chạy):
 *   - CHỈ xử lí yêu cầu GET. Mọi POST (chat, nộp bài, tạo đề...) đi thẳng mạng như cũ.
 *   - Trang HTML và dữ liệu đề: LẤY MẠNG TRƯỚC, mất mạng mới dùng bản đã lưu -> có mạng là luôn mới nhất.
 *   - Không lưu: /api/* (trừ đề làm bài và ảnh hình vẽ), tệp tải về (PDF, Word, zip), trang đăng nhập.
 *   - Không lưu phản hồi lỗi / chuyển hướng (vd chưa đăng nhập bị đưa về /login).
 *   - Đổi PHIEN_BAN là xoá sạch bộ nhớ cũ. Máy chủ có công tắc tắt hẳn (TAT_PWA=1 trong .env -> /sw.js tự gỡ).
 */
const PHIEN_BAN = "nhd-v1";
const TINH = "nhd-tinh-" + PHIEN_BAN;      // thư viện, font, ảnh hình vẽ, tệp tĩnh
const TRANG = "nhd-trang-" + PHIEN_BAN;    // trang làm bài + dữ liệu đề (dùng khi mất mạng)
const OFFLINE = "/static/offline.html";

self.addEventListener("install", function (e) {
    e.waitUntil(caches.open(TINH).then(function (c) { return c.addAll([OFFLINE]); }).then(function () {
        return self.skipWaiting();
    }));
});

self.addEventListener("activate", function (e) {
    e.waitUntil(caches.keys().then(function (ds) {
        return Promise.all(ds.filter(function (k) { return k.indexOf(PHIEN_BAN) === -1; })
            .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); }));
});

function luuDuoc(res) {
    return res && res.ok && !res.redirected && (res.type === "basic" || res.type === "cors");
}

// Lấy bộ nhớ trước (thư viện có ghi phiên bản, ảnh hình vẽ đặt tên theo nội dung: không bao giờ đổi)
function boNhoTruoc(req) {
    return caches.open(TINH).then(function (c) {
        return c.match(req).then(function (co) {
            if (co) return co;
            return fetch(req).then(function (res) {
                if (luuDuoc(res)) c.put(req, res.clone());
                return res;
            });
        });
    });
}

// Trả bộ nhớ ngay (nếu có) và cập nhật ngầm (font, tệp tĩnh không ghi phiên bản)
function boNhoRoiCapNhat(req) {
    return caches.open(TINH).then(function (c) {
        return c.match(req).then(function (co) {
            const moi = fetch(req).then(function (res) {
                if (luuDuoc(res)) c.put(req, res.clone());
                return res;
            }).catch(function () { return co || Response.error(); });
            return co || moi;
        });
    });
}

// Mạng trước, mất mạng thì bản đã lưu (trang làm bài, dữ liệu đề)
function mangTruoc(req, luu) {
    return fetch(req).then(function (res) {
        if (luu && luuDuoc(res)) {
            const ban = res.clone();
            caches.open(TRANG).then(function (c) { c.put(req, ban); });
        }
        return res;
    }).catch(function () {
        return caches.match(req).then(function (co) {
            if (co) return co;
            if (req.mode === "navigate") return caches.match(OFFLINE);
            return Response.error();
        });
    });
}

self.addEventListener("fetch", function (e) {
    const req = e.request;
    if (req.method !== "GET") return;
    let url;
    try { url = new URL(req.url); } catch (x) { return; }

    const cungTrang = url.origin === self.location.origin;
    const p = url.pathname;

    if (cungTrang) {
        if (p.indexOf("/api/exam/hinh/") === 0) { e.respondWith(boNhoTruoc(req)); return; }
        if (p.indexOf("/static/downloads/") === 0 || p === "/sw.js") return;
        if (p.indexOf("/static/") === 0) { e.respondWith(boNhoRoiCapNhat(req)); return; }
        if (p.indexOf("/api/exam/quiz/") === 0) { e.respondWith(mangTruoc(req, true)); return; }
        if (req.mode === "navigate") {
            // Chỉ lưu trang làm bài (mở lại được khi mất mạng); trang khác mất mạng thì hiện trang báo mất mạng
            e.respondWith(mangTruoc(req, p.indexOf("/lam-bai/") === 0));
            return;
        }
        return;                                    // /api/* khác, tệp tải về...: như cũ
    }

    // Thư viện CDN có ghi phiên bản (marked@15.0.12, supabase-js@2, mathjax@3) và font Google
    if (url.hostname === "cdn.jsdelivr.net" && p.indexOf("@") !== -1) {
        e.respondWith(/@\d+\.\d+\.\d+\//.test(p) ? boNhoTruoc(req) : boNhoRoiCapNhat(req));
        return;
    }
    if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
        e.respondWith(boNhoRoiCapNhat(req));
    }
});
