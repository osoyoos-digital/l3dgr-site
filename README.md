# l3dgr.app

The public website for L3dgr. Plain static files served by GitHub Pages: no build step.

## Files

| Path | What it is |
|---|---|
| `index.html` | The landing page |
| `privacy/index.html` | Privacy Policy, served at **https://l3dgr.app/privacy** (the URL for Play Console) |
| `terms/index.html` | Terms of Service, at https://l3dgr.app/terms |
| `404.html` | Page-not-found |
| `assets/site.css`, `assets/site.js` | Styles and the small bits of interaction |
| `assets/img/` | Logo, app screenshots, background video and poster |
| `og.jpg` | The picture shown when the link is shared |
| `CNAME` | Tells GitHub Pages the domain is l3dgr.app |
| `.nojekyll` | Hidden file: tells GitHub Pages to serve the files as they are |

## Common changes

- **Play listing goes live:** in `assets/site.js`, set `PLAY_LIVE = true`. Every Google Play badge and "Get the app" button then links to the store.
- **Legal text:** don't edit `privacy/index.html` or `terms/index.html` by hand. Edit `legal/*.body.html` in the app repo, then run
  `python3 scripts/build-legal.py --site ../l3dgr-site`
  (point `--site` at this folder). The app, its standalone legal pages and this site all get the same text.
- **After changing `site.css` or `site.js`:** bump the `?v=` number where the pages link them (all `.html` files and `build-legal.py` in the app repo), so browsers fetch the new version instead of a cached one.
- **Prices:** in `index.html`, the Plans section (`data-m` = monthly, `data-y` = yearly).
- **Screenshots:** `assets/img/app-*.webp`, 824 × 1830 (Pixel 8 at 2×). Replace them with files of the same name and shape.

## Fonts

Bricolage Grotesque and Manrope load from Google Fonts. To self-host them later, put the `.woff2` files in `assets/fonts/`,
add `@font-face` rules at the top of `site.css`, and remove the three `fonts.googleapis`/`fonts.gstatic` lines from each page's `<head>`.
