/* Lưu ý "bản tiếng Anh mới có đến lớp / chương nào" (cô Lan 14/10/2026).
   Mọi phần tử có thuộc tính data-pham-vi-anh được điền chữ lưu ý lấy từ /api/exam/pham-vi-tieng-anh
   (máy chủ đọc danh sách chương có ngân hàng tiếng Anh, nên tự cập nhật khi thêm chương mới dịch;
   chữ trả về đã theo ngôn ngữ trang đang xem). Phần tử được thêm sau (HTML dựng bằng JS) cũng được điền. */
(function () {
  var luuY = null, dangTai = false;
  function ap() {
    document.querySelectorAll('[data-pham-vi-anh]').forEach(function (e) {
      if (e.textContent !== luuY) { e.textContent = luuY; }
    });
  }
  function dien() {
    if (!document.querySelector('[data-pham-vi-anh]')) { return; }
    if (luuY !== null) { ap(); return; }
    if (dangTai) { return; }
    dangTai = true;
    fetch('/api/exam/pham-vi-tieng-anh', { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (j) { luuY = (j && j.luu_y) || ''; ap(); })
      .catch(function () { dangTai = false; });
  }
  window.dienLuuYTiengAnh = dien;
  document.addEventListener('DOMContentLoaded', dien);
  new MutationObserver(dien).observe(document.documentElement, { childList: true, subtree: true });
})();
