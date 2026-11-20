"""Builds altstable-companion/privacy/index.html from AltStable Companion's PRIVACY.md.

The policy has one source, PRIVACY.md in Spotnick2/AltStableCompanion. This copies it, as it
stands on that repo's main branch (or a local file given as the first argument), into the
page Google's consent screen links to. Rerun it, and commit the page, whenever PRIVACY.md
changes.

Needs the GitHub CLI (gh), signed in: it fetches the file and renders it with GitHub's own
Markdown API, so the page reads like the file does on GitHub.

    python tools/build_privacy.py [path/to/PRIVACY.md]
"""
import base64
import html
import json
import pathlib
import re
import subprocess
import sys

REPO = "Spotnick2/AltStableCompanion"
SITE = pathlib.Path(__file__).resolve().parent.parent
OUT = SITE / "altstable-companion" / "privacy" / "index.html"


def gh(*args, stdin=None):
    return subprocess.run(["gh", *args], input=stdin, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def source():
    if len(sys.argv) > 1:
        return pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    answer = json.loads(gh("api", f"repos/{REPO}/contents/PRIVACY.md"))
    return base64.b64decode(answer["content"]).decode("utf-8")


def main():
    text = source()
    # Links relative to the repo (README.md#...) point at GitHub from this site.
    text = re.sub(r"\]\((?!https?://|#)([^)]+)\)", rf"](https://github.com/{REPO}/blob/main/\1)", text)
    # The page carries its own title; the file's first heading is that title.
    title, _, body = text.partition("\n")
    if not title.startswith("# "):
        sys.exit("PRIVACY.md does not start with its '# ' title")
    rendered = gh("api", "markdown", "--input", "-",
                  stdin=json.dumps({"text": body, "mode": "markdown"}))
    page = TEMPLATE.replace("{title}", html.escape(title[2:].strip())).replace("{body}", rendered.strip())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(SITE)}")


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AltStable Companion privacy policy</title>
  <meta name="description" content="What AltStable Companion reads, keeps and sends, and what it does with your Google data.">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <header class="site">
    <nav>
      <span class="brand">Spotnick2</span>
      <a href="/altstable-companion/">AltStable Companion</a>
      <a href="/altstable-companion/privacy/">Privacy policy</a>
      <a href="https://github.com/Spotnick2/AltStableCompanion">Source code</a>
    </nav>
  </header>
  <main>
    <h1>AltStable Companion: {title}</h1>
{body}
    <footer>
      This page is a copy of
      <a href="https://github.com/Spotnick2/AltStableCompanion/blob/main/PRIVACY.md">PRIVACY.md</a>
      in the app's repository. <a href="/altstable-companion/">AltStable Companion</a> ·
      Not affiliated with or endorsed by Blizzard Entertainment or Google.
    </footer>
  </main>
</body>
</html>
"""

if __name__ == "__main__":
    main()
