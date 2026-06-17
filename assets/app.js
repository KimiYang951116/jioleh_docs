/* ============================================================
   Jio_Leh — Auth Refactor Docs : interactions
   Vanilla JS, zero dependencies.
   ============================================================ */
(function () {
  "use strict";

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var saved = localStorage.getItem("jl-theme");
  if (saved) root.setAttribute("data-theme", saved);

  function toggleTheme() {
    var cur = root.getAttribute("data-theme") === "light" ? "light" : "dark";
    var next = cur === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    localStorage.setItem("jl-theme", next);
  }

  /* ---------- Mobile sidebar ---------- */
  function openNav() { document.body.classList.add("nav-open"); }
  function closeNav() { document.body.classList.remove("nav-open"); }

  /* ---------- Reading progress ---------- */
  var progress = document.getElementById("progress");
  function onScroll() {
    if (!progress) return;
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
    progress.style.width = pct + "%";
  }

  /* ---------- Syntax highlighter (Dart-ish, conservative) ---------- */
  var KEYWORDS = {
    abstract:1, class:1, extends:1, implements:1, with:1, mixin:1, "final":1,
    "const":1, "var":1, "void":1, bool:1, "int":1, "double":1, "num":1, dynamic:1,
    "return":1, "if":1, "else":1, "switch":1, "case":1, "default":1, "for":1,
    "while":1, "do":1, "try":1, "catch":1, "finally":1, "throw":1, async:1,
    await:1, "yield":1, get:1, set:1, "static":1, late:1, "this":1, "super":1,
    "new":1, "null":1, "true":1, "false":1, override:1, "enum":1, required:1,
    "on":1, "as":1, is:1, "in":1, factory:1, "typedef":1, part:1, library:1,
    "import":1, show:1, hide:1, "Function":1
  };

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlight(code) {
    // single pass tokenizer: comments | strings | numbers | identifiers
    var re = /(\/\/[^\n]*)|('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")|\b(\d[\d_]*\.?\d*)\b|([A-Za-z_$][\w$]*)/g;
    var out = "", last = 0, m;
    while ((m = re.exec(code))) {
      out += esc(code.slice(last, m.index));
      last = re.lastIndex;
      if (m[1]) {
        out += '<span class="tok-com">' + esc(m[1]) + "</span>";
      } else if (m[2]) {
        out += '<span class="tok-str">' + esc(m[2]) + "</span>";
      } else if (m[3]) {
        out += '<span class="tok-num">' + esc(m[3]) + "</span>";
      } else {
        var w = m[4];
        var after = code.charAt(re.lastIndex);
        if (KEYWORDS[w]) {
          out += '<span class="tok-kw">' + w + "</span>";
        } else if (/^[A-Z]/.test(w)) {
          out += '<span class="tok-type">' + w + "</span>";
        } else if (after === "(") {
          out += '<span class="tok-fn">' + w + "</span>";
        } else {
          out += esc(w);
        }
      }
    }
    out += esc(code.slice(last));
    return out;
  }

  function applyHighlight() {
    var blocks = document.querySelectorAll("pre.hl > code");
    for (var i = 0; i < blocks.length; i++) {
      var el = blocks[i];
      el.innerHTML = highlight(el.textContent);
    }
  }

  /* ---------- Copy buttons ---------- */
  function wireCopy() {
    var btns = document.querySelectorAll(".cc-copy");
    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var card = btn.closest(".codecard");
        var pre = card ? card.querySelector("pre") : null;
        if (!pre) return;
        var text = pre.innerText;
        navigator.clipboard.writeText(text).then(function () {
          var orig = btn.textContent;
          btn.textContent = "Copied!";
          btn.classList.add("copied");
          setTimeout(function () { btn.textContent = orig; btn.classList.remove("copied"); }, 1400);
        });
      });
    });
  }

  /* ---------- Build "On this page" TOC + scroll spy ---------- */
  function buildTOC() {
    var toc = document.getElementById("toc");
    var article = document.querySelector(".content-inner");
    if (!toc || !article) return;
    var heads = article.querySelectorAll("h2, h3");
    if (heads.length < 2) { toc.style.display = "none"; return; }

    var html = '<div class="toc-label">On this page</div>';
    var items = [];
    heads.forEach(function (h) {
      if (!h.id) return;
      var cls = h.tagName === "H3" ? "h3" : "h2";
      html += '<a class="' + cls + '" href="#' + h.id + '">' + h.dataset.toc + "</a>";
      items.push(h);
    });
    toc.innerHTML = html;

    var links = toc.querySelectorAll("a");
    function spy() {
      var pos = window.scrollY + 110;
      var current = items[0];
      for (var i = 0; i < items.length; i++) {
        if (items[i].offsetTop <= pos) current = items[i];
      }
      links.forEach(function (a) {
        a.classList.toggle("active", a.getAttribute("href") === "#" + (current && current.id));
      });
    }
    window.addEventListener("scroll", spy, { passive: true });
    spy();
  }

  /* ---------- Sidebar filter ---------- */
  function wireFilter() {
    var input = document.getElementById("sideFilter");
    if (!input) return;
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      document.querySelectorAll(".sidebar .nav-link").forEach(function (a) {
        var t = a.dataset.search || a.textContent;
        a.classList.toggle("hide", q && t.toLowerCase().indexOf(q) === -1);
      });
    });
  }

  /* ---------- Wire up ---------- */
  document.addEventListener("DOMContentLoaded", function () {
    applyHighlight();
    wireCopy();
    buildTOC();
    wireFilter();

    var tbtn = document.getElementById("themeBtn");
    if (tbtn) tbtn.addEventListener("click", toggleTheme);
    var mbtn = document.getElementById("menuBtn");
    if (mbtn) mbtn.addEventListener("click", openNav);
    var bd = document.querySelector(".backdrop");
    if (bd) bd.addEventListener("click", closeNav);
    document.querySelectorAll(".sidebar .nav-link").forEach(function (a) {
      a.addEventListener("click", closeNav);
    });

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    // keyboard: "/" focuses filter
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
        var f = document.getElementById("sideFilter");
        if (f) { e.preventDefault(); f.focus(); }
      }
    });
  });
})();
