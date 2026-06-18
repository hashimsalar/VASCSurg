/* ============================================================
   UNM VASCULAR SURGERY — FIELD GUIDE
   Shared behaviour for every page.
   ============================================================ */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var slice = function (n) { return Array.prototype.slice.call(n); };

  /* ---------- Mobile drawer ---------- */
  var sidebar = document.getElementById("sidebar");
  var toggle = document.getElementById("navToggle");
  var scrim = document.getElementById("scrim");
  function openNav() { sidebar.classList.add("open"); scrim.classList.add("show"); }
  function closeNav() { sidebar.classList.remove("open"); scrim.classList.remove("show"); }
  if (toggle) toggle.addEventListener("click", function () {
    sidebar.classList.contains("open") ? closeNav() : openNav();
  });
  if (scrim) scrim.addEventListener("click", closeNav);

  /* ---------- Mark active page + build per-page sub-nav ---------- */
  var path = location.pathname.split("/").pop() || "index.html";
  if (path === "") path = "index.html";
  var links = slice(document.querySelectorAll(".sb-link"));
  var activeLink = null;
  links.forEach(function (a) {
    var href = (a.getAttribute("href") || "").split("/").pop();
    if (href === path) { a.classList.add("active"); activeLink = a; }
  });

  // Build sub-nav from this page's <section id data-title>
  var sections = slice(document.querySelectorAll("main section[id][data-title]"));
  var subLinks = {};
  if (activeLink && sections.length) {
    var ul = document.createElement("ul");
    ul.className = "sb-sub";
    sections.forEach(function (sec) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + sec.id;
      a.textContent = sec.getAttribute("data-title");
      a.addEventListener("click", function () {
        if (window.innerWidth <= 1000) closeNav();
      });
      subLinks[sec.id] = a;
      li.appendChild(a);
      ul.appendChild(li);
    });
    activeLink.insertAdjacentElement("afterend", ul);
  }

  /* ---------- Scroll-spy over sections ---------- */
  if (sections.length && "IntersectionObserver" in window) {
    var visible = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) visible[e.target.id] = e.boundingClientRect.top;
        else delete visible[e.target.id];
      });
      var ids = Object.keys(visible);
      if (ids.length) {
        ids.sort(function (x, y) { return Math.abs(visible[x]) - Math.abs(visible[y]); });
        Object.keys(subLinks).forEach(function (id) { subLinks[id].classList.remove("current"); });
        if (subLinks[ids[0]]) subLinks[ids[0]].classList.add("current");
      }
    }, { rootMargin: "-12% 0px -72% 0px", threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Reading progress ---------- */
  var bar = document.getElementById("progress");
  function onScroll() {
    if (bar) {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    }
    if (toTop) {
      if (window.scrollY > 620) toTop.classList.add("show");
      else toTop.classList.remove("show");
    }
  }

  /* ---------- Back to top ---------- */
  var toTop = document.getElementById("toTop");
  if (toTop) toTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Reveal on scroll ---------- */
  var revealEls = slice(document.querySelectorAll(".reveal, .stagger, .sec-head"));
  if (reduce || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var ro = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); obs.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { ro.observe(el); });
    requestAnimationFrame(function () {
      revealEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) el.classList.add("in");
      });
    });
  }

  /* ---------- Count-up stats ---------- */
  var counters = slice(document.querySelectorAll("[data-count]"));
  function runCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduce) { el.textContent = target + suffix; return; }
    var dur = 1100, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (counters.length) {
    if (reduce || !("IntersectionObserver" in window)) {
      counters.forEach(runCount);
    } else {
      var co = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { runCount(e.target); obs.unobserve(e.target); }
        });
      }, { threshold: 0.6 });
      counters.forEach(function (c) { co.observe(c); });
    }
  }
})();
