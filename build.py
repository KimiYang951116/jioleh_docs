#!/usr/bin/env python3
"""
Static-site generator for the Jio_Leh Authentication Refactor documentation.

Run:  python3 build.py
It emits index.html + 01..06-*.html into this directory, sharing one
sidebar / topbar / theme so navigation stays consistent.

Why a generator instead of 7 hand-written pages: the chrome (nav, head,
footer, prev/next) is identical everywhere, so it lives in ONE place
(SHELL) and every page only supplies its own body. Edit content below,
re-run, commit the regenerated HTML.
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_DOCS = "https://github.com/KimiYang951116/jioleh-auth-refactor-docs"
REPO_APP  = "https://github.com/KimiYang951116/JioLeh"

# The design system (CSS) and behaviour (JS) live in assets/ as readable
# source, but are INLINED into every page at build time so the site stays
# 100% self-contained (no extra requests, deploys anywhere). Edit the files
# in assets/, then re-run this script.
def _read_asset(name):
    with open(os.path.join(HERE, "assets", name), encoding="utf-8") as f:
        return f.read()

STYLES = _read_asset("styles.css")
APPJS  = _read_asset("app.js")

# ----------------------------------------------------------------------
# Page order (drives sidebar + prev/next)
#
# The site documents two refactor PRs as two "books". Each book is a
# section with its own overview (num "00") + ordered change pages. The
# sidebar groups them; prev/next stays within a book.
# ----------------------------------------------------------------------
SECTIONS = [
    {
        "book": "Auth Service Refactor",
        "changes_label": "The six changes",
        "pages": [
            ("index.html",                        "00", "Overview & Index"),
            ("01-auth-service-interface.html",    "01", "AuthService Interface"),
            ("02-service-provider-di.html",       "02", "ServiceProvider DI"),
            ("03-auth-gate-split.html",           "03", "AuthGate Split"),
            ("04-race-condition-fix.html",        "04", "Race Condition Fix"),
            ("05-error-logging.html",             "05", "Error Logging"),
            ("06-directory-reorganization.html",  "06", "Directory Reorg"),
        ],
    },
    {
        "book": "Auth & Profile Widget Refactor",
        "changes_label": "The eleven changes",
        "pages": [
            ("widget-refactor.html",               "00", "Overview & Index"),
            ("widget-01-theme-tokens.html",        "01", "Theme Tokens"),
            ("widget-02-field-atoms.html",         "02", "Field Atoms"),
            ("widget-03-birthday-row.html",        "03", "BirthdayRow"),
            ("widget-04-onboarding-widgets.html",  "04", "onboarding_widgets on atoms"),
            ("widget-05-app-primary-button.html",  "05", "AppPrimaryButton"),
            ("widget-06-login-widgets.html",       "06", "login_widgets tokenization"),
            ("widget-07-login-snackbar.html",      "07", "login_page snackbar"),
            ("widget-08-username-rule.html",       "08", "UsernameRule"),
            ("widget-09-birthday-merge.html",      "09", "Birthday merge"),
            ("widget-10-profile-edit.html",        "10", "profile_edit on atoms"),
            ("widget-11-relocate-onboarding.html", "11", "Relocate onboarding"),
        ],
    },
]

# Flat list (build loop + lookups)
PAGES = [p for s in SECTIONS for p in s["pages"]]

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)

def code(src, name="", lang="dart"):
    src = src.strip("\n")
    hl = " hl" if lang not in ("text", "") else ""
    name_html = '<span class="cc-name">%s</span>' % esc(name) if name else ""
    return (
        '<div class="codecard"><div class="cc-head">'
        '<span class="cc-dots"><i></i><i></i><i></i></span>'
        '%s<span class="cc-lang">%s</span>'
        '<button class="cc-copy" type="button">Copy</button>'
        '</div><pre class="%s"><code>%s</code></pre></div>'
        % (name_html, esc(lang) if lang else "", hl.strip(), esc(src))
    )

def diagram(src, label="diagram"):
    return ('<div class="diagram"><span class="dlabel">%s</span><pre>%s</pre></div>'
            % (esc(label), esc(src.strip("\n"))))

ICONS = {
    "good": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "bad":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    "warn": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/></svg>',
    "quote":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 7h4v4H8c0 2 1 3 3 3v2c-3 0-5-2-5-5V7zm8 0h4v4h-3c0 2 1 3 3 3v2c-3 0-5-2-5-5V7z"/></svg>',
}

def callout(body, kind="info", label=""):
    icon = ICONS.get(kind, ICONS["info"])
    lab = '<span class="label">%s</span> ' % esc(label) if label else ""
    return ('<div class="callout callout-%s"><span class="ic">%s</span>'
            '<div><p>%s%s</p></div></div>' % (kind, icon, lab, body))

def h2(hid, label):
    return ('<h2 id="%s" data-toc="%s">%s<a class="anchor" href="#%s" aria-label="Link to section">#</a></h2>'
            % (hid, esc(label), esc(label), hid))

def h3(hid, label):
    return ('<h3 id="%s" data-toc="%s">%s<a class="anchor" href="#%s" aria-label="Link to section">#</a></h3>'
            % (hid, esc(label), esc(label), hid))

def table(headers, rows):
    th = "".join("<th>%s</th>" % c for c in headers)
    body = ""
    for r in rows:
        body += "<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>"
    return ('<div class="tablewrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (th, body))

CH = lambda: '<span class="verdict v-chosen">CHOSEN</span>'
RJ = lambda t="Rejected": '<span class="verdict v-reject">%s</span>' % esc(t)
NE = lambda t: '<span class="verdict v-neutral">%s</span>' % esc(t)
WN = lambda t: '<span class="verdict v-warn">%s</span>' % esc(t)

def cc(s):  # inline code, angle-bracket safe
    return "<code>%s</code>" % esc(s)

# ----------------------------------------------------------------------
# Shared shell
# ----------------------------------------------------------------------
IC_THEME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
IC_MENU  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'
IC_GH    = '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.6 7.6 0 0 1 2-.27c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>'

SHELL = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<meta name="description" content="%%DESC%%">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
%%STYLES%%
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%231d3d28'/><text x='16' y='22' font-size='15' font-family='monospace' font-weight='bold' fill='%2346c47e' text-anchor='middle'>JL</text></svg>">
<script>try{var t=localStorage.getItem('jl-theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}</script>
</head>
<body>
<div id="progress"></div>
<header class="topbar">
  <button class="icon-btn" id="menuBtn" aria-label="Open navigation">%%IC_MENU%%</button>
  <a class="brand" href="index.html">
    <span class="logo">JL</span>
    <span>Jio_Leh <span class="sub">/ Auth Refactor</span></span>
  </a>
  <span class="spacer"></span>
  <nav class="tnav">
    <a href="index.html">Auth Service</a>
    <a href="widget-refactor.html">Widget Refactor</a>
  </nav>
  <a class="icon-btn" href="%%REPO_APP%%" target="_blank" rel="noopener" aria-label="App repository">%%IC_GH%%</a>
  <button class="icon-btn" id="themeBtn" aria-label="Toggle theme">%%IC_THEME%%</button>
</header>
<div class="backdrop"></div>
<div class="shell">
  <aside class="sidebar">
    <input id="sideFilter" class="side-filter" type="text" placeholder="Filter sections  ( / )" aria-label="Filter sections">
    %%SIDEBAR%%
  </aside>
  <main class="content">
    <div class="content-inner">
      %%BODY%%
      %%PREVNEXT%%
      <footer class="foot">
        <p>Engineering design notes for the
        <a href="%%REPO_APP%%" target="_blank" rel="noopener">Jio_Leh</a> refactors ·
        Flutter + Supabase · Generated from the change write-ups ·
        <a href="%%REPO_DOCS%%" target="_blank" rel="noopener">site source</a>.</p>
      </footer>
    </div>
  </main>
  <aside class="toc" id="toc"></aside>
</div>
%%APPJS%%
</body>
</html>
"""

def sidebar(active):
    out = ""
    for si, sec in enumerate(SECTIONS):
        mt = ' style="margin-top:18px"' if si > 0 else ''
        out += '<div class="side-label"%s>%s</div>' % (mt, esc(sec["book"]))
        for pi, (fn, num, title) in enumerate(sec["pages"]):
            if pi == 1:
                out += ('<div class="side-label" style="margin-top:18px">%s</div>'
                        % esc(sec["changes_label"]))
            cls = "nav-link active" if fn == active else "nav-link"
            out += ('<a class="%s" href="%s" data-search="%s %s">'
                    '<span class="num">%s</span><span>%s</span></a>'
                    % (cls, fn, esc(title), num, num, esc(title)))
    return out

def prevnext(active):
    # prev/next stays within the active page's own book.
    pages = next(s["pages"] for s in SECTIONS if active in [p[0] for p in s["pages"]])
    idx = [i for i, p in enumerate(pages) if p[0] == active][0]
    if idx > 0:
        fn, num, title = pages[idx - 1]
        prev_a = ('<a href="%s"><div class="dir">&larr; Previous</div>'
                  '<div class="ttl">%s &middot; %s</div></a>' % (fn, num, esc(title)))
    else:
        prev_a = '<span style="flex:1"></span>'
    if idx < len(pages) - 1:
        fn, num, title = pages[idx + 1]
        next_a = ('<a class="next" href="%s"><div class="dir">Next &rarr;</div>'
                  '<div class="ttl">%s &middot; %s</div></a>' % (fn, num, esc(title)))
    else:
        next_a = '<span style="flex:1"></span>'
    return '<nav class="pagenav">%s%s</nav>' % (prev_a, next_a)

def render(active, title, desc, body):
    out = SHELL
    out = out.replace("%%TITLE%%", esc(title))
    out = out.replace("%%DESC%%", esc(desc))
    out = out.replace("%%IC_MENU%%", IC_MENU)
    out = out.replace("%%IC_THEME%%", IC_THEME)
    out = out.replace("%%IC_GH%%", IC_GH)
    out = out.replace("%%REPO_APP%%", REPO_APP)
    out = out.replace("%%REPO_DOCS%%", REPO_DOCS)
    out = out.replace("%%STYLES%%", "<style>" + STYLES + "</style>")
    out = out.replace("%%APPJS%%", "<script>" + APPJS + "</script>")
    out = out.replace("%%SIDEBAR%%", sidebar(active))
    out = out.replace("%%PREVNEXT%%", prevnext(active))
    out = out.replace("%%BODY%%", body)   # last: body may contain other text
    return out

def crumbs(label):
    return ('<div class="crumbs"><a href="index.html">Auth Refactor</a> '
            '&nbsp;/&nbsp; %s</div>' % esc(label))

# ----------------------------------------------------------------------
# Import page bodies (kept in content.py to keep this file readable)
# ----------------------------------------------------------------------
import content as C

PAGE_DEFS = {
    "index.html":                       (C.TITLE_00, C.DESC_00, C.body_00),
    "01-auth-service-interface.html":   (C.TITLE_01, C.DESC_01, C.body_01),
    "02-service-provider-di.html":      (C.TITLE_02, C.DESC_02, C.body_02),
    "03-auth-gate-split.html":          (C.TITLE_03, C.DESC_03, C.body_03),
    "04-race-condition-fix.html":       (C.TITLE_04, C.DESC_04, C.body_04),
    "05-error-logging.html":            (C.TITLE_05, C.DESC_05, C.body_05),
    "06-directory-reorganization.html": (C.TITLE_06, C.DESC_06, C.body_06),

    # ---- Book 2: Auth & Profile Widget Refactor ----
    "widget-refactor.html":               (C.TITLE_W00, C.DESC_W00, C.body_w00),
    "widget-01-theme-tokens.html":        (C.TITLE_W01, C.DESC_W01, C.body_w01),
    "widget-02-field-atoms.html":         (C.TITLE_W02, C.DESC_W02, C.body_w02),
    "widget-03-birthday-row.html":        (C.TITLE_W03, C.DESC_W03, C.body_w03),
    "widget-04-onboarding-widgets.html":  (C.TITLE_W04, C.DESC_W04, C.body_w04),
    "widget-05-app-primary-button.html":  (C.TITLE_W05, C.DESC_W05, C.body_w05),
    "widget-06-login-widgets.html":       (C.TITLE_W06, C.DESC_W06, C.body_w06),
    "widget-07-login-snackbar.html":      (C.TITLE_W07, C.DESC_W07, C.body_w07),
    "widget-08-username-rule.html":       (C.TITLE_W08, C.DESC_W08, C.body_w08),
    "widget-09-birthday-merge.html":      (C.TITLE_W09, C.DESC_W09, C.body_w09),
    "widget-10-profile-edit.html":        (C.TITLE_W10, C.DESC_W10, C.body_w10),
    "widget-11-relocate-onboarding.html": (C.TITLE_W11, C.DESC_W11, C.body_w11),
}

# expose helpers to content module
C.bind(globals())

def main():
    for fn, _num, _title in PAGES:
        title, desc, body_fn = PAGE_DEFS[fn]
        html_out = render(fn, title, desc, body_fn())
        with open(os.path.join(HERE, fn), "w", encoding="utf-8") as f:
            f.write(html_out)
        print("wrote", fn, "(%d bytes)" % len(html_out))

if __name__ == "__main__":
    main()
