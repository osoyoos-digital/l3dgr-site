#!/usr/bin/env python3
"""Builds the Terms of Service and Privacy Policy from legal/*.body.html.

- legal/terms.html and legal/privacy.html: standalone pages to host publicly (Play Console needs a public
  privacy policy URL).
- The website's copies (optional): with --site DIR, also writes DIR/privacy/index.html and DIR/terms/index.html
  in the website's own style (served at l3dgr.app/privacy and l3dgr.app/terms).
- The app's own copy: the LEGAL object between /*LEGAL:START*/ and /*LEGAL:END*/ in each HTML file given
  (www/index.html by default), so the documents also open offline inside the app.

Edit the .body.html files, then run:  python3 scripts/build-legal.py [--site ../l3dgr-site] [more.html ...]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGAL = os.path.join(ROOT, 'legal')
DOCS = {'terms': 'Terms of Service', 'privacy': 'Privacy Policy'}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>L3dgr: {title}</title>
<meta name="description" content="L3dgr {title}">
<style>
:root{{color-scheme:light dark;--bg:#EEF1EE;--surface:#FBFCFB;--ink:#16201B;--ink2:#4A5650;--muted:#747F79;--line:#DCE2DD;--accent:#1F6B52;--soft:#DCEBE4}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0E1311;--surface:#171E1B;--ink:#E8EEEA;--ink2:#B3BFB8;--muted:#85918B;--line:#27312C;--accent:#4FBF93;--soft:#1A3029}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-text-size-adjust:100%}}
header{{max-width:720px;margin:0 auto;padding:28px 20px 0;display:flex;align-items:center;gap:16px}}
header .brand{{font-weight:800;font-size:18px;letter-spacing:-.01em;color:var(--ink);text-decoration:none}}
header nav{{margin-left:auto;display:flex;gap:16px;font-size:14px;font-weight:600}}
header nav a{{color:var(--muted);text-decoration:none}}
header nav a[aria-current]{{color:var(--accent)}}
main{{max-width:720px;margin:16px auto 48px;padding:28px 20px;background:var(--surface);border:1px solid var(--line);border-radius:18px}}
@media (min-width:760px){{main{{padding:40px 48px}}}}
h1{{font-size:30px;line-height:1.15;letter-spacing:-.02em;margin:0 0 4px}}
h2{{font-size:17px;margin:32px 0 6px}}
p,li{{color:var(--ink2)}}
p{{margin:0 0 12px}}
ul{{margin:0 0 12px;padding-left:22px}}
li{{margin:4px 0}}
b{{color:var(--ink)}}
a{{color:var(--accent)}}
.eff{{color:var(--muted);font-size:14px;margin-bottom:20px}}
.tldr{{background:var(--soft);border-radius:14px;padding:16px 18px 6px;margin:0 0 8px}}
.tldr p,.tldr li{{color:var(--ink)}}
footer{{max-width:720px;margin:0 auto 40px;padding:0 20px;color:var(--muted);font-size:13px}}
</style>
</head>
<body>
<header><a class="brand" href="privacy.html">L3dgr</a><nav><a href="terms.html"{terms_cur}>Terms</a><a href="privacy.html"{privacy_cur}>Privacy</a></nav></header>
<main>
{body}
</main>
<footer>L3dgr, a personal budgeting app.</footer>
</body>
</html>
"""


# The website's version: same text, the site's header, footer and stylesheet. Keep in step with the site's index.html.
SITE_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · L3dgr</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0E1311">
<link rel="canonical" href="https://l3dgr.app/{key}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon-64.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Manrope:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header class="nav solid">
  <div class="wrap">
    <a class="brand" href="/" aria-label="L3dgr home"><img src="/assets/img/logo.png" alt="" width="32" height="32">L3dgr</a>
    <a class="btn btn-ghost btn-sm" href="/" style="margin-left:auto">Back to home</a>
  </div>
</header>
<main class="doc">
  <div class="wrap">
    <nav class="tabs" aria-label="Legal"><a href="/privacy"{privacy_cur}>Privacy Policy</a><a href="/terms"{terms_cur}>Terms of Service</a></nav>
    <article>
{body}
    </article>
  </div>
</main>
<footer class="site">
  <div class="wrap">
    <div>
      <a class="brand" href="/"><img src="/assets/img/logo.png" alt="" width="32" height="32">L3dgr</a>
      <p>A simple spending tracker by Osoyoos Digital, an independent developer in British Columbia, Canada.</p>
    </div>
    <div>
      <h4>App</h4>
      <ul><li><a href="/#how">How it works</a></li><li><a href="/#features">Features</a></li><li><a href="/#plans">Plans</a></li><li><a href="/#faq">FAQ</a></li></ul>
    </div>
    <div>
      <h4>Legal</h4>
      <ul><li><a href="/privacy">Privacy Policy</a></li><li><a href="/terms">Terms of Service</a></li></ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul><li><a href="mailto:hello@l3dgr.app">hello@l3dgr.app</a></li></ul>
    </div>
    <div class="legal"><span>© 2026 Osoyoos Digital</span><span>Google Play and the Google Play logo are trademarks of Google LLC.</span></div>
  </div>
</footer>
</body>
</html>
"""
SITE_DESC = {'privacy': 'How L3dgr handles your information: your budget stays on your phone. No ads, no tracking, no analytics.',
             'terms': 'The terms for using L3dgr, a simple spending tracker for Android.'}


def read(k):
    with open(os.path.join(LEGAL, f'{k}.body.html'), encoding='utf-8') as f:
        return f.read().strip()


def main(targets, site=None):
    bodies = {k: read(k) for k in DOCS}
    for k, title in DOCS.items():
        html = PAGE.format(title=title, body=bodies[k],
                           terms_cur=' aria-current="page"' if k == 'terms' else '',
                           privacy_cur=' aria-current="page"' if k == 'privacy' else '')
        with open(os.path.join(LEGAL, f'{k}.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print('wrote', f'legal/{k}.html')
        if site:
            os.makedirs(os.path.join(site, k), exist_ok=True)
            page = SITE_PAGE.format(title=title, key=k, desc=SITE_DESC[k], body=bodies[k],
                                    terms_cur=' aria-current="page"' if k == 'terms' else '',
                                    privacy_cur=' aria-current="page"' if k == 'privacy' else '')
            with open(os.path.join(site, k, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(page)
            print('wrote', os.path.join(site, k, 'index.html'))
    # in the app the title sits in the popup's own header, and links open outside it
    app = {k: re.sub(r'<h1>.*?</h1>\s*', '', b, count=1, flags=re.S).replace('<a href=', '<a target="_blank" rel="noopener" href=')
           for k, b in bodies.items()}
    block = '/*LEGAL:START*/const LEGAL = ' + json.dumps(app, ensure_ascii=False).replace('</', '<\\/') + ';/*LEGAL:END*/'
    for t in targets:
        with open(t, encoding='utf-8') as f:
            s = f.read()
        n = len(re.findall(r'/\*LEGAL:START\*/.*?/\*LEGAL:END\*/', s, flags=re.S))
        if n != 1:
            sys.exit(f'{t}: expected one LEGAL block, found {n}')
        s = re.sub(r'/\*LEGAL:START\*/.*?/\*LEGAL:END\*/', lambda m: block, s, flags=re.S)
        with open(t, 'w', encoding='utf-8') as f:
            f.write(s)
        print('updated', t)


if __name__ == '__main__':
    args, site = sys.argv[1:], None
    if '--site' in args:
        i = args.index('--site')
        if i + 1 >= len(args):
            sys.exit('--site needs the website folder, e.g. --site ../l3dgr-site')
        site = args[i + 1]; del args[i:i + 2]
    main(args or [os.path.join(ROOT, 'www', 'index.html')], site)
