# Jio_Leh — Authentication Refactor Docs

A small static documentation **website** that records the `refactor/authentication`
work on [Jio_Leh](https://github.com/KimiYang951116/JioLeh) (Flutter + Supabase)
in depth — not just *what* changed, but the full thinking behind every decision:
the problems we found, every option weighed (naïve → preferred), the trade-offs,
the chosen fix, the resulting code, and the tests.

It exists so that **future-us and teammates** can understand, six months from now,
why the auth layer is shaped the way it is.

## 🔗 View the site

Once GitHub Pages is enabled (see below), the site lives at:

> **https://kimiyang951116.github.io/jioleh-auth-refactor-docs/**

To preview locally, just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## 📚 What's inside

| Page | Change | Core idea |
| ---- | ------ | --------- |
| `index.html` | **00 — Overview & Index** | The story, the method, the principles, the commit timeline |
| `01-auth-service-interface.html` | **01 — AuthService Interface** | Testability via abstraction (Dependency Inversion) |
| `02-service-provider-di.html` | **02 — ServiceProvider DI** | Be handed dependencies, don't grab globals |
| `03-auth-gate-split.html` | **03 — AuthGate Split** | One widget, three jobs → model + link holder + thin widget (SRP) |
| `04-race-condition-fix.html` | **04 — Race Condition Fix** | Newest async result wins; don't notify after disposal |
| `05-error-logging.html` | **05 — Error Logging** | Observability: stop swallowing the cause |
| `06-directory-reorganization.html` | **06 — Directory Reorg** | Organize by feature; keep folders cohesive |

Each change page follows the same shape: **the problem → the options ladder
(with pros/cons/verdict) → the decision and why → the code → the tests → the result.**

## ✏️ Editing / rebuilding

The HTML pages are **generated** so that the shared chrome (sidebar, top bar,
theme, prev/next) stays consistent. Don't hand-edit the `.html` files — edit the
source and regenerate:

```
build.py       → the page shell + templating (sidebar, head, footer, prev/next)
content.py     → all the actual prose, tables, code samples and diagrams
assets/styles.css → the design system (light + dark themes)
assets/app.js  → theme toggle, scroll-spy TOC, copy buttons, syntax highlighter
```

```bash
python3 build.py     # regenerates index.html + 01..06-*.html
```

No dependencies — plain Python 3, no build tools, no node_modules. The site is
100% static (HTML/CSS/vanilla JS) and hosts anywhere.

## 🚀 Enabling GitHub Pages

1. Repo **Settings → Pages**
2. **Source:** *Deploy from a branch*
3. **Branch:** `main`, folder `/ (root)` → **Save**
4. Wait ~1 minute, then open the URL above.

(The `.nojekyll` file tells Pages to serve the files as-is.)

---

*Built as living documentation for the Jio_Leh auth refactor. Behaviour for the
user was unchanged across all six commits — these were pure internal quality
improvements: testability, correctness, observability, and organization.*
