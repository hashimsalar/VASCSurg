# Vascular Surgery Field Guide

A static, multi-page field guide to the vascular surgery service for residents, sub-interns and medical students. Plain HTML, CSS and JavaScript. There are no dependencies and no framework, so any static host (Vercel, GitHub Pages, Netlify) can serve the folder as-is.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home: role-based reading paths, contents, the vascular mindset |
| `first-day.html` | Your first day |
| `rounds.html` | Rounds and presenting |
| `charting.html` | History, exam and charting (note templates) |
| `ctv-icu.html` | The CTV ICU |
| `on-call.html` | On call and cross-cover |
| `foundations.html` | Foundations |
| `presentations.html` | Major presentations |
| `operations.html` | Open operations |
| `endovascular.html` | The endovascular playbook |
| `devices.html` | Wires, catheters and devices |
| `questions.html` | Questions you'll be asked |
| `reference.html` | Quick reference |

Shared files live in `assets/`: `styles.css`, `app.js`, `search-index.js` (generated), `favicon.svg` and `portrait.jpg`.

## Editing

Each page has marker comments such as `<!-- @nav --> … <!-- /@nav -->`. Whatever sits between the markers is generated. That includes the head, top bar, chapter list, "On this page" lists, previous/next links and the footer. Edit the content inside `<main>`, then run:

```bash
python3 scripts/build.py
```

The build re-stamps the shared pieces on every page and regenerates the search index. To add, remove or reorder a page, edit the `GROUPS` list at the top of `scripts/build.py` and rebuild.

### Writing conventions

- Every top-level `<section>` needs `class="sec"`, a unique `id` and a short `data-title`. These feed the "On this page" lists and search.
- `data-bed="arterial" | "venous" | "both"` sets the colored bar on the section heading: red for arterial, blue for venous, split for both. Leave it off for general topics.
- Callouts: `note flag` (red flag), `note pearl`, `note mnem` (mnemonic), `note tip` (resident tip), `note local` (confirm locally), `note plain`.
- Teaching questions use `<details class="qa">`, with the question in `<summary>` and the answer in `<div class="qa-a">`.
- Note templates use `<figure class="template">` with a `<pre>`. A "Copy template" button is added automatically.
- Use US spelling and sentence case. Do not name the institution.

## Preview locally

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173.
