#!/usr/bin/env python3
"""Check provenance integrity, evidence references, generated output, and local links."""
import ast
import hashlib
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'demonstrated','supported_but_incomplete','hypothesis_postulate','unresolved','rejected'}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids=set(); self.links=[]; self.errors=[]; self.title=False; self.lang=False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='html': self.lang=bool(a.get('lang'))
        if tag=='title': self.title=True
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('duplicate id '+a['id'])
            self.ids.add(a['id'])
        for attr in ('href','src'):
            if attr in a: self.links.append(a[attr])

def main():
    errors=[]
    provenance=json.loads((ROOT/'data/provenance.json').read_text())
    claims=json.loads((ROOT/'data/claims.json').read_text())
    sources=json.loads((ROOT/'data/sources.json').read_text())
    raw=(ROOT/provenance['specimen']['path']).read_bytes()
    text=raw.decode('utf-8')
    if hashlib.sha256(raw).hexdigest()!=provenance['specimen']['sha256']: errors.append('Frozen specimen checksum mismatch')
    if len(raw)!=provenance['specimen']['size_bytes']: errors.append('Specimen byte count mismatch')
    if len(text.split())!=provenance['specimen']['word_count']: errors.append('Specimen word count mismatch')
    if not text.startswith('THE WARREN REPORT: UNREDACTED TRUTH EDITION\n'): errors.append('Specimen opening absent')
    if not text.rstrip().endswith('Exported from Medium on August 19, 2025.'): errors.append('Specimen footer absent')
    source_ids={s['id'] for s in sources}
    if len(source_ids)!=len(sources): errors.append('Duplicate source identifiers')
    claim_ids={c['id'] for c in claims}
    if len(claim_ids)!=len(claims): errors.append('Duplicate claim identifiers')
    for c in claims:
        if c['status'] not in ALLOWED: errors.append(c['id']+': invalid status')
        if c['specimen_quote'] not in text: errors.append(c['id']+': quote not found in frozen specimen')
        if not set(c['source_ids'])<=source_ids: errors.append(c['id']+': missing source')
        if any(not c[k] for k in ['title','category','finding','basis','next_test']): errors.append(c['id']+': incomplete finding')
    for s in sources:
        if urlsplit(s['url']).scheme!='https': errors.append(s['id']+': source must use HTTPS')
        if not s['supports'] or not s['limitation']: errors.append(s['id']+': source lacks scope')
    for p in (ROOT/'scripts').glob('*.py'):
        try: ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
        except SyntaxError as exc: errors.append(str(exc))
    generated=subprocess.run([sys.executable,str(ROOT/'scripts/build_site.py'),'--check'],capture_output=True,text=True)
    if generated.returncode: errors.append(generated.stderr.strip() or generated.stdout.strip())
    pages={p.resolve():Page(p.read_text(encoding='utf-8')) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
    links_checked=0
    for p,parsed in pages.items():
        if not parsed.lang or not parsed.title: errors.append(str(p.relative_to(ROOT))+': missing title or language')
        errors.extend(str(p.relative_to(ROOT))+': '+e for e in parsed.errors)
        for target in parsed.links:
            url=urlsplit(target)
            if url.scheme or url.netloc: continue
            if url.path.startswith('/'): errors.append(f'{p.name}: root-relative path breaks project hosting: {target}'); continue
            dest=(p.parent/unquote(url.path)).resolve() if url.path else p
            if not dest.is_relative_to(ROOT.resolve()): errors.append(f'{p.name}: link escapes project: {target}'); continue
            if not dest.exists(): errors.append(f'{p.name}: missing local target {target}'); continue
            if url.fragment and dest in pages and unquote(url.fragment) not in pages[dest].ids:
                errors.append(f'{p.name}: missing fragment {target}')
            links_checked+=1
    for p in list((ROOT/'docs').glob('*.md'))+[ROOT/'README.md',ROOT/'CONTRIBUTING.md',ROOT/'specimen/README.md']:
        for _,target in re.findall(r'\[([^\]]*)\]\(([^\s)]+)\)',p.read_text(encoding='utf-8')):
            url=urlsplit(target)
            if not url.scheme and not url.netloc and url.path:
                dest=(p.parent/unquote(url.path)).resolve()
                if not dest.exists(): errors.append(f'{p.name}: missing Markdown target {target}')
    manifest=ROOT/'SHA256SUMS.txt'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            digest, path=line.split('  ',1)
            p=ROOT/path
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
                errors.append('Package digest mismatch: '+path)
    if errors:
        print('\n'.join('ERROR: '+e for e in errors)); raise SystemExit(1)
    print(f'PASS: {len(claims)} claims, {len(sources)} sources, {len(pages)} HTML pages, {links_checked} local HTML links.')
    print('PASS: specimen SHA-256, quote correspondence, source references, Python syntax, deterministic generated output.')
    print('Scope: local structural checks only; no browser rendering or live-model replication is asserted.')

if __name__=='__main__': main()
