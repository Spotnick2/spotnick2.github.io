# spotnick2.github.io

The GitHub Pages site at <https://spotnick2.github.io/>: plain HTML, no build step, no Jekyll
(`.nojekyll`).

- `index.html`: the projects page.
- `altstable-companion/`: AltStable Companion's homepage, the one its Google OAuth consent
  screen names.
- `altstable-companion/privacy/`: its privacy policy, the page the consent screen links to.
  It is generated: the source is
  [PRIVACY.md](https://github.com/Spotnick2/AltStableCompanion/blob/main/PRIVACY.md) in the
  app's repository. Whenever that file changes, run `python tools/build_privacy.py` (needs
  `gh`, signed in) and commit the page.
- The screenshots in `altstable-companion/` are copies of the app repository's
  `docs/images`, with real names blurred.

Google Search Console verifies this site for the consent screen's authorized domain: keep the
verification file Google gave (`google*.html` at the root) in place.
