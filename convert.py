#!/usr/bin/env python3
"""
Convert uncertainty-collapse.md to professional HTML and PDF.
Figures embedded as base64. Floating TOC with burger menu. Dark mode toggle.
"""

import base64, re, os, sys
from pathlib import Path

import markdown

SRC_DIR = Path("/mnt/user-data/outputs")
MD_FILE = SRC_DIR / "uncertainty-collapse.md"
FIG1 = SRC_DIR / "uncertainty-collapse-fig1.jpg"
FIG2 = SRC_DIR / "uncertainty-collapse-fig2.jpg"
OUT_HTML = SRC_DIR / "uncertainty-collapse.html"
OUT_PDF = SRC_DIR / "uncertainty-collapse.pdf"


def b64_img(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/jpeg;base64,{data}"


def parse_md(text: str, fig1_b64: str, fig2_b64: str) -> tuple:
    """Return (html_body, toc_entries)."""
    # Replace markdown image refs with base64
    text = text.replace(
        "![Figure 1. Predicted temporal signature of uncertainty collapse.](uncertainty-collapse-fig1.jpg)",
        f'<img src="{fig1_b64}" alt="Figure 1" class="figure" />'
    )
    text = text.replace(
        "![Figure 2. Three-dimensional representation of the post-training landscape.](uncertainty-collapse-fig2.jpg)",
        f'<img src="{fig2_b64}" alt="Figure 2" class="figure" />'
    )

    # Convert MD to HTML
    html = markdown.markdown(text, extensions=["extra", "smarty"])

    # Build TOC from h1-h3 and inject IDs
    toc = []
    counter = [0]

    def heading_replacer(m):
        tag = m.group(1)
        content = m.group(2)
        counter[0] += 1
        slug = f"section-{counter[0]}"
        level = int(tag[1])
        clean = re.sub(r"<[^>]+>", "", content).strip()
        toc.append((level, slug, clean))
        return f'<{tag} id="{slug}">{content}</{tag}>'

    html = re.sub(r"<(h[1-3])>(.*?)</\1>", heading_replacer, html, flags=re.DOTALL)

    return html, toc


def build_toc_html(toc: list) -> str:
    items = []
    for level, slug, title in toc:
        indent = (level - 1) * 16
        cls = f"toc-h{level}"
        items.append(f'<a href="#{slug}" class="{cls}" style="padding-left:{indent}px">{title}</a>')
    return "\n".join(items)


def build_full_html(body: str, toc_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Uncertainty Collapse in Post-Trained Language Models</title>
<style>
/* ===== RESET & BASE ===== */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --bg: #fafaf8;
  --fg: #1a1a1a;
  --fg-secondary: #555;
  --accent: #c44e52;
  --accent2: #4c72b0;
  --amber: #e8a838;
  --border: #ddd;
  --code-bg: #f4f0ec;
  --blockquote-bg: #f9f7f4;
  --blockquote-border: #d4c5a9;
  --toc-bg: #ffffff;
  --toc-shadow: rgba(0,0,0,0.15);
  --link: #4c72b0;
  --figure-border: #e0dcd4;
}}

html.dark {{
  --bg: #1a1a1e;
  --fg: #d8d8d0;
  --fg-secondary: #999;
  --border: #333;
  --code-bg: #252528;
  --blockquote-bg: #222225;
  --blockquote-border: #555;
  --toc-bg: #222225;
  --toc-shadow: rgba(0,0,0,0.5);
  --link: #7da2d4;
  --figure-border: #444;
}}

/* ===== TYPOGRAPHY ===== */
body {{
  font-family: "Bitstream Charter", "Charter", "Georgia", serif;
  font-size: 18px;
  line-height: 1.75;
  color: var(--fg);
  background: var(--bg);
  max-width: 700px;
  margin: 0 auto;
  padding: 48px 24px 120px;
  transition: background 0.3s, color 0.3s;
}}

h1 {{
  font-size: 1.85em;
  line-height: 1.25;
  margin: 0 0 8px;
  letter-spacing: -0.01em;
}}

h2 {{
  font-size: 1.35em;
  margin: 2.4em 0 0.7em;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
  letter-spacing: -0.005em;
}}

h3 {{
  font-size: 1.1em;
  margin: 1.8em 0 0.5em;
  color: var(--fg);
}}

p {{
  margin: 0 0 1.05em;
}}

a {{
  color: var(--link);
  text-decoration: none;
}}
a:hover {{
  text-decoration: underline;
}}

strong {{
  font-weight: 600;
}}

em {{
  font-style: italic;
}}

hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 2.5em 0;
}}

/* ===== FRONT MATTER ===== */
h1 + p, h1 + p + p, h1 + p + p + p {{
  color: var(--fg-secondary);
  font-size: 0.95em;
}}

/* ===== BLOCKQUOTES (figure captions) ===== */
blockquote {{
  background: var(--blockquote-bg);
  border-left: 3px solid var(--blockquote-border);
  padding: 14px 18px;
  margin: 0 0 1.2em;
  font-size: 0.88em;
  line-height: 1.6;
  color: var(--fg-secondary);
  border-radius: 2px;
}}

blockquote p {{
  margin: 0;
}}

/* ===== FIGURES ===== */
img.figure {{
  display: block;
  max-width: 100%;
  margin: 1.5em auto 0.6em;
  border: 1px solid var(--figure-border);
  border-radius: 3px;
}}

/* ===== CODE ===== */
code {{
  font-family: "SF Mono", "Consolas", "Menlo", monospace;
  font-size: 0.85em;
  background: var(--code-bg);
  padding: 2px 5px;
  border-radius: 3px;
}}

/* ===== PREDICTIONS & BOLD LABELS ===== */
p > strong:first-child {{
  color: var(--fg);
}}

/* ===== BURGER MENU & TOC ===== */
.menu-btn {{
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 1001;
  width: 44px;
  height: 44px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--toc-bg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  box-shadow: 0 2px 8px var(--toc-shadow);
  transition: background 0.3s, border-color 0.3s;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}}

.toc-panel {{
  position: fixed;
  top: 0;
  left: -340px;
  width: 320px;
  height: 100vh;
  background: var(--toc-bg);
  border-right: 1px solid var(--border);
  z-index: 1000;
  overflow-y: auto;
  padding: 72px 20px 40px;
  transition: left 0.3s ease, background 0.3s;
  box-shadow: 4px 0 20px var(--toc-shadow);
}}

.toc-panel.open {{
  left: 0;
}}

.toc-panel .toc-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}}

.toc-panel .toc-title {{
  font-family: Georgia, serif;
  font-size: 0.95em;
  font-weight: 600;
  color: var(--fg);
  letter-spacing: 0.03em;
  text-transform: uppercase;
}}

.dark-toggle {{
  cursor: pointer;
  font-size: 18px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 10px;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  transition: background 0.3s, border-color 0.3s;
}}
.dark-toggle:hover {{
  border-color: var(--fg-secondary);
}}

.toc-panel a {{
  display: block;
  padding: 5px 0;
  font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 0.82em;
  color: var(--fg-secondary);
  text-decoration: none;
  line-height: 1.45;
  border-radius: 3px;
  transition: color 0.2s;
}}

.toc-panel a:hover {{
  color: var(--fg);
}}

.toc-panel a.toc-h1 {{
  font-weight: 600;
  font-size: 0.88em;
  color: var(--fg);
  margin-top: 6px;
}}

.toc-panel a.toc-h2 {{
  font-weight: 600;
  font-size: 0.84em;
  margin-top: 4px;
}}

.toc-panel a.toc-h3 {{
  font-weight: 400;
}}

.overlay {{
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  z-index: 999;
}}

.overlay.active {{
  display: block;
}}

/* ===== PRINT / PDF ===== */
@media print {{
  .menu-btn, .toc-panel, .overlay {{ display: none !important; }}
  body {{
    max-width: none;
    padding: 0;
    font-size: 11pt;
    line-height: 1.55;
  }}
  h2 {{ page-break-before: auto; }}
  img.figure {{ max-width: 95%; }}
  blockquote {{ break-inside: avoid; }}
  @page {{
    size: A4;
    margin: 22mm 20mm 25mm 20mm;
    @bottom-center {{
      content: counter(page);
      font-family: Georgia, serif;
      font-size: 9pt;
      color: #999;
    }}
  }}
}}
</style>
</head>
<body>

<!-- Burger menu button -->
<button class="menu-btn" onclick="toggleToc()" aria-label="Table of contents">☰</button>

<!-- Overlay -->
<div class="overlay" onclick="toggleToc()"></div>

<!-- TOC panel -->
<nav class="toc-panel">
  <div class="toc-header">
    <span class="toc-title">Contents</span>
    <button class="dark-toggle" onclick="toggleDark()" aria-label="Toggle dark mode">🌙</button>
  </div>
  {toc_html}
</nav>

<!-- Body -->
{body}

<script>
function toggleToc() {{
  document.querySelector('.toc-panel').classList.toggle('open');
  document.querySelector('.overlay').classList.toggle('active');
}}

// Close TOC on link click
document.querySelectorAll('.toc-panel a').forEach(a => {{
  a.addEventListener('click', () => {{
    document.querySelector('.toc-panel').classList.remove('open');
    document.querySelector('.overlay').classList.remove('active');
  }});
}});

function toggleDark() {{
  document.documentElement.classList.toggle('dark');
  const btn = document.querySelector('.dark-toggle');
  btn.textContent = document.documentElement.classList.contains('dark') ? '☀️' : '🌙';
}}
</script>
</body>
</html>"""


def main():
    print("Reading markdown...")
    md_text = MD_FILE.read_text(encoding="utf-8")

    print("Encoding figures...")
    fig1_b64 = b64_img(FIG1)
    fig2_b64 = b64_img(FIG2)

    print("Parsing markdown to HTML...")
    body_html, toc = parse_md(md_text, fig1_b64, fig2_b64)
    toc_html = build_toc_html(toc)
    full_html = build_full_html(body_html, toc_html)

    # HTML: sans-serif for screen reading
    html_screen = full_html.replace(
        '"Bitstream Charter", "Charter", "Georgia", serif',
        '"Carlito", "Calibri", "Helvetica Neue", "Inter", sans-serif'
    ).replace(
        'font-size: 18px',
        'font-size: 17px'
    ).replace(
        'line-height: 1.75',
        'line-height: 1.8'
    )

    print(f"Writing HTML → {OUT_HTML}")
    OUT_HTML.write_text(html_screen, encoding="utf-8")

    # PDF: serif for archival/academic
    print(f"Generating PDF → {OUT_PDF}")
    from weasyprint import HTML
    HTML(string=full_html, base_url=str(SRC_DIR)).write_pdf(str(OUT_PDF))

    print("Done.")
    html_size = OUT_HTML.stat().st_size / 1024
    pdf_size = OUT_PDF.stat().st_size / 1024
    print(f"  HTML: {html_size:.0f} KB")
    print(f"  PDF:  {pdf_size:.0f} KB")


if __name__ == "__main__":
    main()
