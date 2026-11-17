#!/usr/bin/env python3
"""Check internal links, image files, HTML headings and accidental tracking."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1] / "dist"

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.assets=[]
        self.ids=set()
        self.h1=0
        self.title=False
        self.lang=False
        self.image_missing_alt=[]
        self.third_party_scripts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="html": self.lang=a.get("lang")=="es"
        if tag=="title": self.title=True
        if tag=="h1": self.h1+=1
        if a.get("id"): self.ids.add(a["id"])
        if tag=="a" and "href" in a: self.links.append(a["href"])
        if tag in ("img","script") and "src" in a: self.assets.append(a["src"])
        if tag=="link" and a.get("rel") in ("stylesheet","icon"): self.assets.append(a["href"])
        if tag=="img" and "alt" not in a: self.image_missing_alt.append(a.get("src",""))
        if tag=="script" and urlparse(a.get("src","")).netloc: self.third_party_scripts.append(a["src"])

pages={}
errors=[]
for f in ROOT.rglob("*.html"):
    p=Page()
    p.feed(f.read_text(encoding="utf-8"))
    pages[f.resolve()]=p
    if p.h1!=1: errors.append(f"{f.relative_to(ROOT)}: expected one h1, got {p.h1}")
    if not p.title or not p.lang: errors.append(f"{f.relative_to(ROOT)}: missing title/language")
    if p.image_missing_alt: errors.append(f"{f.relative_to(ROOT)}: missing image alt")
    if p.third_party_scripts: errors.append(f"{f.relative_to(ROOT)}: third-party scripts")

for f,p in pages.items():
    for href in p.links+p.assets:
        u=urlparse(href)
        if u.scheme or u.netloc: continue
        if not href or href=="#": errors.append(f"{f.name}: placeholder link")
        target=(ROOT/unquote(u.path.lstrip("/"))) if u.path.startswith("/") else (f.parent/unquote(u.path) if u.path else f)
        if target.is_dir(): target=target/"index.html"
        target=target.resolve()
        if not target.exists():
            errors.append(f"{f.relative_to(ROOT)}: missing {href}")
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f"{f.relative_to(ROOT)}: missing anchor {href}")

js=(ROOT/"assets/site.js").read_text()
for unwanted in ["localStorage","sessionStorage","document.cookie","navigator.sendBeacon","fetch("]:
    if unwanted in js: errors.append("Unexpected persistence/network code: "+unwanted)
print(json.dumps({"pages_checked":len(pages),"errors":errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
