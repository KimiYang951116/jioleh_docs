# Jio_Leh — Engineering Design Notes

A small static documentation **website** that records refactor work on
[Jio_Leh](https://github.com/KimiYang951116/JioLeh) (Flutter + Supabase) in depth
— not just *what* changed, but the full thinking behind every decision: the
problems we found, every option weighed (naïve → preferred), the trade-offs, the
chosen fix, the resulting code, and the tests.

It exists so that **future-us and teammates** can understand, six months from now,
why the code is shaped the way it is. The site hosts two design logs ("books"):

1. **Auth Service Refactor** (`refactor/authentication`) — the service/auth-gate
   layer: testability, DI, the gate split, the race fix, logging, folder layout.
2. **Auth & Profile Widget Refactor** (`refactor/auth-frontend`, PR #123) — the
   widget layer: a design-system foundation (theme tokens + atoms) and every
   onboarding/profile/login screen rebuilt on top of it.

## 🔗 View the site

Once GitHub Pages is enabled (see below), the site lives at:

> **https://kimiyang951116.github.io/jioleh-auth-refactor-docs/**

To preview locally, just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## 📚 What's inside

**Book 1 — Auth Service Refactor**

| Page | Change | Core idea |
| ---- | ------ | --------- |
| `index.html` | **00 — Overview & Index** | The story, the method, the principles, the commit timeline |
| `01-auth-service-interface.html` | **01 — AuthService Interface** | Testability via abstraction (Dependency Inversion) |
| `02-service-provider-di.html` | **02 — ServiceProvider DI** | Be handed dependencies, don't grab globals |
| `03-auth-gate-split.html` | **03 — AuthGate Split** | One widget, three jobs → model + link holder + thin widget (SRP) |
| `04-race-condition-fix.html` | **04 — Race Condition Fix** | Newest async result wins; don't notify after disposal |
| `05-error-logging.html` | **05 — Error Logging** | Observability: stop swallowing the cause |
| `06-directory-reorganization.html` | **06 — Directory Reorg** | Organize by feature; keep folders cohesive |

**Book 2 — Auth & Profile Widget Refactor** (PR #123)

| Page | Change | Core idea |
| ---- | ------ | --------- |
| `widget-refactor.html` | **00 — Overview & Index** | The big picture, the 4-layer model, the cross-cutting principles |
| `widget-01-theme-tokens.html` | **01 — Theme Tokens** | Tokenize colors/radii/shadows/heights so a value lives once |
| `widget-02-field-atoms.html` | **02 — Field Atoms** | AppSectionLabel, AppFieldBox, AppTextField — when a shared visual deserves its own layer |
| `widget-03-birthday-row.html` | **03 — BirthdayRow** | Extract the shared row, then unify to the stronger version |
| `widget-04-onboarding-widgets.html` | **04 — onboarding_widgets on atoms** | A ~215-line build() becomes ~45 lines of composition |
| `widget-05-app-primary-button.html` | **05 — AppPrimaryButton** | The CTA atom that owns its loading spinner (rule of three) |
| `widget-06-login-widgets.html` | **06 — login_widgets tokenization** | Tokenize hex — and decline to merge the Google button |
| `widget-07-login-snackbar.html` | **07 — login_page snackbar** | Tokenize repetition; leave genuine one-offs inline |
| `widget-08-username-rule.html` | **08 — UsernameRule** | One rule object so hint/formatters/regex can't disagree |
| `widget-09-birthday-merge.html` | **09 — Birthday merge** | One strict parser kills two silent bugs; share pieces, not forms |
| `widget-10-profile-edit.html` | **10 — profile_edit on atoms** | The biggest monolith (~510 lines) more than halves |
| `widget-11-relocate-onboarding.html` | **11 — Relocate onboarding** | Organize by "what changes together" |

Each change page follows the same shape: **the context → the problem → the options
(with pros/cons/verdict) → the decision and why → what changed → the trade-offs → the result.**

## ✏️ Editing / rebuilding

The HTML pages are **generated** so that the shared chrome (sidebar, top bar,
theme, prev/next) stays consistent. Don't hand-edit the `.html` files — edit the
source and regenerate:

```
build.py       → the page shell + templating (sidebar, top bar, footer, prev/next)
                 and the SECTIONS list (the two books + their page order)
content.py     → all the actual prose, tables, code samples and diagrams
assets/styles.css → the design system (light + dark themes)
assets/app.js  → theme toggle, scroll-spy TOC, copy buttons, syntax highlighter
```

`assets/styles.css` and `assets/app.js` are the real source for the look and
behaviour; `build.py` **inlines** them into every page at build time, so each
published `.html` stays fully self-contained (no extra requests, hosts anywhere).

```bash
python3 build.py     # regenerates all 19 pages (Book 1: index + 01..06, Book 2: widget-*)
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
