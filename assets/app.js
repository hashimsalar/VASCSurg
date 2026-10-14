/* ============================================================
   Vascular Surgery Field Guide — shared behaviour
   Drawer nav, theme, search, scroll-spy, copy buttons,
   role tracks, angiogram highlights. No dependencies.
   ============================================================ */
(function () {
  "use strict";
  var doc = document;
  var root = doc.documentElement;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      if (val === null) localStorage.removeItem(key); else localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  /* ---------- Theme ---------- */
  $$("[data-theme-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      if (!current) {
        current = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }
      var next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store("vfg-theme", next);
      btn.setAttribute("aria-label", next === "dark" ? "Switch to light mode" : "Switch to dark mode");
    });
  });

  /* ---------- Drawer navigation (small screens) ---------- */
  var rail = $("#rail");
  var scrim = $(".scrim");
  var openers = $$("[data-nav-open]");
  var lastFocus = null;
  function setNav(open) {
    if (!rail) return;
    rail.classList.toggle("open", open);
    if (scrim) scrim.classList.toggle("show", open);
    openers.forEach(function (b) { b.setAttribute("aria-expanded", open ? "true" : "false"); });
    if (open) {
      lastFocus = doc.activeElement;
      var cur = $('.rail-link[aria-current="page"]', rail) || $("a, button", rail);
      if (cur) cur.focus({ preventScroll: true });
      if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "center" });
    } else if (lastFocus) {
      lastFocus.focus({ preventScroll: true });
    }
  }
  openers.forEach(function (b) { b.addEventListener("click", function () { setNav(!rail.classList.contains("open")); }); });
  $$("[data-nav-close]").forEach(function (b) { b.addEventListener("click", function () { setNav(false); }); });
  if (scrim) scrim.addEventListener("click", function () { setNav(false); });
  doc.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && rail && rail.classList.contains("open")) setNav(false);
  });

  /* ---------- Scroll-spy for "On this page" ---------- */
  var asideLinks = $$(".aside a[href^='#']");
  if (asideLinks.length && "IntersectionObserver" in window) {
    var map = {};
    asideLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var visible = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) visible[e.target.id] = e.target.getBoundingClientRect().top;
        else delete visible[e.target.id];
      });
      var ids = Object.keys(visible);
      if (!ids.length) return;
      ids.sort(function (x, y) { return visible[x] - visible[y]; });
      asideLinks.forEach(function (a) { a.classList.remove("current"); });
      if (map[ids[0]]) map[ids[0]].classList.add("current");
    }, { rootMargin: "-15% 0px -65% 0px", threshold: 0 });
    $$(".sec[id]").forEach(function (s) { if (map[s.id]) spy.observe(s); });
  }

  /* ---------- Back to top ---------- */
  var toTop = $(".to-top");
  if (toTop) {
    var onScroll = function () { toTop.classList.toggle("show", window.scrollY > 900); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
      var skip = $("#main");
      if (skip) skip.focus({ preventScroll: true });
    });
  }

  /* ---------- Copy buttons on templates ---------- */
  $$(".template").forEach(function (fig) {
    var pre = $("pre", fig);
    var head = $(".template-head", fig);
    if (!pre || !head || !navigator.clipboard) return;
    var btn = doc.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy template";
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(pre.innerText.replace(/ /g, " ")).then(function () {
        btn.textContent = "Copied";
        btn.classList.add("done");
        setTimeout(function () { btn.textContent = "Copy template"; btn.classList.remove("done"); }, 1800);
      }, function () {
        btn.textContent = "Select and copy";
      });
    });
    head.appendChild(btn);
  });

  /* ---------- Question tools: reveal all / hide all ---------- */
  $$("[data-qa-all]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("data-qa-all") === "open";
      var scope = btn.closest(".sec") || doc;
      $$(".qa", scope).forEach(function (d) { d.open = open; });
    });
  });
  $$(".qa > summary").forEach(function (s) {
    if (!$(".reveal-hint", s)) {
      var hint = doc.createElement("span");
      hint.className = "reveal-hint";
      hint.setAttribute("aria-hidden", "true");
      s.appendChild(hint);
    }
  });
  window.addEventListener("beforeprint", function () { $$("details").forEach(function (d) { d.open = true; }); });

  /* ---------- Role tracks (home) ---------- */
  var tabs = $$(".track-tab");
  if (tabs.length) {
    var panels = $$(".track-panel");
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
      });
      panels.forEach(function (p) { p.hidden = p.id !== tab.getAttribute("aria-controls"); });
      if (focus) tab.focus();
      store("vfg-track", tab.id);
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var n = null;
        if (e.key === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
    var saved = store("vfg-track");
    var start = (saved && doc.getElementById(saved)) || tabs[0];
    select(start);
  }

  /* ---------- Angiogram: list <-> pins ---------- */
  var angio = $(".angio");
  if (angio) {
    var items = $$("ol li[data-v]", angio);
    var light = function (v, on) {
      items.forEach(function (li) { li.classList.toggle("hl", on && li.getAttribute("data-v") === v); });
      $$(".pin", angio).forEach(function (p) { p.classList.toggle("hl", on && p.getAttribute("data-v") === v); });
    };
    items.forEach(function (li) {
      var v = li.getAttribute("data-v");
      li.addEventListener("mouseenter", function () { light(v, true); });
      li.addEventListener("mouseleave", function () { light(v, false); });
    });
    $$(".pin", angio).forEach(function (p) {
      var v = p.getAttribute("data-v");
      p.addEventListener("mouseenter", function () { light(v, true); });
      p.addEventListener("mouseleave", function () { light(v, false); });
    });
  }

  /* ---------- Search ---------- */
  var dlg = null, input = null, list = null, indexLoaded = false, results = [], sel = -1;
  var appScript = $('script[src*="assets/app.js"]');
  var base = appScript ? appScript.getAttribute("src").replace(/assets\/app\.js.*$/, "") : "";
  var indexVer = appScript ? appScript.getAttribute("data-index") : null;

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }

  function buildDialog() {
    dlg = doc.createElement("dialog");
    dlg.className = "search-dlg";
    dlg.setAttribute("aria-label", "Search the guide");
    dlg.innerHTML =
      '<div class="search-top">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input class="search-input" type="search" placeholder="Search: HIT, Rutherford, endoleak, Bentson…" aria-label="Search the guide" autocomplete="off" spellcheck="false">' +
      '<button class="icon-btn" type="button" data-search-close aria-label="Close search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>' +
      "</div>" +
      '<ul class="search-results" role="listbox" aria-label="Results"></ul>' +
      '<p class="search-foot">Searches every page. Use the arrow keys and Enter to open a result.</p>';
    doc.body.appendChild(dlg);
    input = $(".search-input", dlg);
    list = $(".search-results", dlg);
    $("[data-search-close]", dlg).addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    input.addEventListener("input", function () { run(input.value); });
    input.addEventListener("keydown", function (e) {
      var links = $$("a", list);
      if (e.key === "ArrowDown" && links.length) { e.preventDefault(); sel = Math.min(sel + 1, links.length - 1); mark(links); }
      else if (e.key === "ArrowUp" && links.length) { e.preventDefault(); sel = Math.max(sel - 1, 0); mark(links); }
      else if (e.key === "Enter") {
        var target = links[sel >= 0 ? sel : 0];
        if (target) { e.preventDefault(); location.href = target.href; dlg.close(); }
      }
    });
    list.addEventListener("click", function (e) { if (e.target.closest("a")) dlg.close(); });
  }
  function mark(links) {
    links.forEach(function (a, i) { a.classList.toggle("sel", i === sel); a.setAttribute("aria-selected", i === sel ? "true" : "false"); });
    if (links[sel]) links[sel].scrollIntoView({ block: "nearest" });
  }
  function loadIndex(cb) {
    if (indexLoaded || window.SEARCH_INDEX) { indexLoaded = true; cb(); return; }
    var s = doc.createElement("script");
    s.src = base + "assets/search-index.js" + (indexVer ? "?v=" + indexVer : "");
    s.onload = function () { indexLoaded = true; cb(); };
    s.onerror = function () { list.innerHTML = '<li><p class="search-empty">Search is unavailable offline. Use the contents menu instead.</p></li>'; };
    doc.head.appendChild(s);
  }
  function snippet(text, terms) {
    var t = norm(text), at = -1;
    for (var i = 0; i < terms.length && at < 0; i++) at = t.indexOf(terms[i]);
    var start = Math.max(0, at - 60);
    var out = (start > 0 ? "…" : "") + text.slice(start, start + 180) + (text.length > start + 180 ? "…" : "");
    var html = esc(out);
    terms.forEach(function (term) {
      if (term.length < 2) return;
      var re = new RegExp("(" + term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
      html = html.replace(re, "<mark>$1</mark>");
    });
    return html;
  }
  function run(q) {
    sel = -1;
    var terms = norm(q).split(/\s+/).filter(Boolean);
    if (!terms.length) { list.innerHTML = '<li><p class="search-empty">Type a term, a drug, a classification or a device.</p></li>'; return; }
    var idx = window.SEARCH_INDEX || [];
    results = [];
    idx.forEach(function (r) {
      var title = norm(r.t), body = norm(r.x), page = norm(r.p), score = 0, ok = true;
      terms.forEach(function (term) {
        var inT = title.indexOf(term) > -1, inB = body.indexOf(term) > -1, inP = page.indexOf(term) > -1;
        if (!inT && !inB && !inP) ok = false;
        score += (inT ? 10 : 0) + (inP ? 3 : 0) + (inB ? 1 + Math.min(4, body.split(term).length - 1) : 0);
      });
      if (ok) results.push({ r: r, s: score });
    });
    results.sort(function (a, b) { return b.s - a.s; });
    if (!results.length) {
      list.innerHTML = '<li><p class="search-empty">Nothing matches “' + esc(q) + '”. Try a shorter word or a synonym (for example, “ALI” or “acute limb”).</p></li>';
      return;
    }
    list.innerHTML = results.slice(0, 30).map(function (o) {
      var r = o.r;
      return '<li><a href="' + base + r.u + '" role="option"><span class="r-page">' + esc(r.p) + '</span><span class="r-title">' + esc(r.t) + '</span><span class="r-snip">' + snippet(r.x, terms) + "</span></a></li>";
    }).join("");
  }
  function openSearch() {
    if (!dlg) buildDialog();
    if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
    setNav(false);
    input.select();
    loadIndex(function () { run(input.value); });
  }
  $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", openSearch); });
  doc.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    var typing = tag === "input" || tag === "textarea" || e.target.isContentEditable;
    if (!typing && (e.key === "/" || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k"))) {
      e.preventDefault();
      openSearch();
    }
  });
})();
