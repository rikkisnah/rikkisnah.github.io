#!/usr/bin/env python3
"""Build one ready-to-paste humanize prompt per voice.

Reads humanize-prompt-base.md, fills the {{VOICE}} slot from each file in
voices/, and writes prompts/humanize-prompt-<voice>.md. The {{TEXT}} slot is
left as [PASTE TEXT HERE] for the user to fill.

Run from this folder:  python3 build.py
"""
from pathlib import Path

here = Path(__file__).resolve().parent
base = (here / "humanize-prompt-base.md").read_text(encoding="utf-8")
out_dir = here / "prompts"
out_dir.mkdir(exist_ok=True)

for voice_file in sorted((here / "voices").glob("*.md")):
    voice = voice_file.read_text(encoding="utf-8").strip()
    prompt = base.replace("{{VOICE}}", voice).replace("{{TEXT}}", "[PASTE TEXT HERE]")
    out = out_dir / f"humanize-prompt-{voice_file.stem}.md"
    out.write_text(prompt, encoding="utf-8")
    print(f"wrote {out.relative_to(here)} ({len(prompt.split())} words)")

# A voice-free version that keeps the source's own voice.
neutral = base.replace(
    "{{VOICE}}", "keep the voice the source text already has"
).replace("{{TEXT}}", "[PASTE TEXT HERE]")
(out_dir / "humanize-prompt-no-voice.md").write_text(neutral, encoding="utf-8")
print("wrote prompts/humanize-prompt-no-voice.md")
