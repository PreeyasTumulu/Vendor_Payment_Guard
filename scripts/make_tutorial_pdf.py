"""Rebuild TUTORIAL.pdf from TUTORIAL.md.

Markdown -> HTML with pandoc, then HTML -> PDF with Microsoft Edge (headless).
The Mermaid diagrams are drawn by mermaid.js inside Edge, so this build step needs internet once.
The agent itself (the notebook) never needs internet.

Usage:  python scripts/make_tutorial_pdf.py
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HEADER = """
<style>
  body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45;
         max-width: 900px; margin: 0 auto; color: #1f2328; }
  h1 { font-size: 22pt; margin-bottom: 0; }
  h2 { font-size: 15pt; border-bottom: 2px solid #1565c0; padding-bottom: 3px; margin-top: 28px; break-after: avoid; }
  h3 { font-size: 12pt; break-after: avoid; }
  table { border-collapse: collapse; margin: 8px 0; break-inside: avoid; }
  th, td { border: 1px solid #c9ccd1; padding: 3px 6px; font-size: 9pt; vertical-align: top; }
  th { background: #eef3fb; }
  table { width: 100%; }
  td code, th code { white-space: normal; word-break: break-word; }
  code { font-family: Consolas, monospace; font-size: 9pt; background: #f3f4f6; padding: 0 2px; }
  pre { background: #f6f8fa; padding: 8px 10px; font-size: 8.5pt; white-space: pre-wrap; break-inside: avoid; }
  pre code { background: none; }
  .diagram { text-align: center; margin: 10px 0; break-inside: avoid; }
  .diagram svg { max-width: 100%; height: auto; }
  blockquote { border-left: 4px solid #1565c0; margin: 8px 0; padding: 2px 12px; background: #f5f8fd; }
  img { max-width: 100%; break-inside: avoid; }
  @page { margin: 14mm 12mm; }
</style>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: false, theme: "neutral" });
  let n = 0;
  for (const block of document.querySelectorAll("pre.mermaid")) {      // one diagram at a time
    const { svg } = await mermaid.render("diagram" + n++, block.textContent);
    block.outerHTML = '<div class="diagram">' + svg + "</div>";
  }
</script>
"""

def main():
    header_file = ROOT / "_header.html"
    html_file = ROOT / "_tutorial.html"
    pdf_file = ROOT / "TUTORIAL.pdf"
    header_file.write_text(HEADER, encoding="utf-8")
    try:
        subprocess.run(["pandoc", "TUTORIAL.md", "-o", html_file.name, "--standalone",
                        "--metadata", "pagetitle=Vendor Payment Guard - Tutorial",
                        "--include-in-header", header_file.name],
                       cwd=ROOT, check=True)
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=20000", f"--print-to-pdf={pdf_file}",
                        html_file.as_uri()],
                       check=True)
    finally:
        header_file.unlink(missing_ok=True)
        html_file.unlink(missing_ok=True)
    print("wrote", pdf_file)

if __name__ == "__main__":
    main()
