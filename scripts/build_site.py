#!/usr/bin/env python3
"""Build the static archive from local JSON, Markdown, and the frozen specimen.

Uses Python's standard library. Does not contact a network or modify the specimen.
"""
import argparse
import csv
import html
import io
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {
    'demonstrated': 'Demonstrated',
    'supported_but_incomplete': 'Supported but incomplete',
    'hypothesis_postulate': 'Hypothesis / postulate',
    'unresolved': 'Unresolved',
    'rejected': 'Rejected as stated',
}
REPO = 'https://github.com/enuminous/Extrauniversal-Warren-Report'

def esc(value):
    return html.escape(str(value), quote=True)

def read_json(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def local_link(url):
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url):
        return url
    url = url.replace('specimen/README.md', 'specimen.html')
    url = re.sub(r'(^|/)README\.md(?=#|$)', r'\1index.html', url)
    return re.sub(r'\.md(?=#|$)', '.html', url)

def inline(text):
    """Render a deliberately small, escaped Markdown subset used in this repo."""
    tokens = []
    def hold(markup):
        tokens.append(markup)
        return f'\x00{len(tokens)-1}\x00'
    text = re.sub(r'`([^`]+)`', lambda m: hold('<code>'+esc(m[1])+'</code>'), text)
    text = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',
                  lambda m: hold(f'<a href="{esc(local_link(m[2]))}">{esc(m[1])}</a>'), text)
    text = esc(text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    return re.sub(r'\x00(\d+)\x00', lambda m: tokens[int(m[1])], text)

def markdown(text):
    lines = text.splitlines()
    out, paragraph = [], []
    i = 0
    def flush():
        if paragraph:
            out.append('<p>'+inline(' '.join(paragraph))+'</p>')
            paragraph.clear()
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            flush(); i += 1; continue
        if line.startswith('```'):
            flush(); i += 1; code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            out.append('<pre><code>'+esc('\n'.join(code))+'</code></pre>'); i += 1; continue
        if line.startswith('$$'):
            flush()
            out.append('<div class="equation" role="math" aria-label="Probability of disclosure by time t equals q times one minus exponential negative lambda t">P(T ≤ t) = q (1 − e<sup>−λt</sup>)</div>')
            i += 1; continue
        heading = re.match(r'^(#{1,6}) (.+)$', line)
        if heading:
            flush(); level = len(heading[1]); title = heading[2]
            out.append(f'<h{level} id="{slug(title)}">{inline(title)}</h{level}>'); i += 1; continue
        if line.startswith('|') and i+1 < len(lines) and re.match(r'^\|[\s:|\-]+\|$', lines[i+1]):
            flush()
            headers = [c.strip() for c in line.strip('|').split('|')]
            i += 2; rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip('|').split('|')]); i += 1
            out.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable comparison table"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>')
            continue
        if re.match(r'^(- |\d+\. )', line):
            flush(); ordered = bool(re.match(r'^\d+\.', line)); tag = 'ol' if ordered else 'ul'; items=[]
            pattern = r'^\d+\. ' if ordered else r'^- '
            while i < len(lines) and re.match(pattern, lines[i]):
                items.append('<li>'+inline(re.sub(pattern, '', lines[i]))+'</li>'); i += 1
            out.append(f'<{tag}>'+''.join(items)+f'</{tag}>'); continue
        paragraph.append(line); i += 1
    flush()
    return '\n'.join(out)

def shell(title, body, prefix='', specimen=False, doc=False):
    desc = 'A submitted ChatGPT-4o hallucination specimen, with provenance limits, primary sources, and an evidence audit.'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Extra Universal Kennedy</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex,follow">' if specimen else ''}
<meta name="color-scheme" content="light"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/app.js" defer></script></head>
<body class="{'document-page' if doc else 'archive-page'}"><a class="skip" href="#main">Skip to content</a>
<div class="context-strip">AI HALLUCINATION CASE STUDY <span>Submitted specimen · Unverified model provenance</span></div>
<header class="site-header"><a class="brand" href="{prefix}index.html" aria-label="Extra Universal Kennedy home"><span class="brand-mark" aria-hidden="true">EU<span>K</span></span><span>Extra Universal<br><strong>Kennedy</strong></span></a>
<nav aria-label="Main navigation"><a href="{prefix}index.html#evidence">Evidence</a><a href="{prefix}docs/CASE_STUDY.html">Case study</a><a href="{prefix}specimen.html">Specimen</a><a href="{prefix}docs/SOURCES.html">Sources</a><a href="{REPO}">GitHub ↗</a></nav></header>
<main id="main">{body}</main>
<footer><div><strong>Extra Universal Kennedy</strong><p>Case EUK-001 · Evidence reviewed October 13, 2026.<br>Submitted by Matthew Chenoweth Wright. Analysis prepared with AI assistance.</p></div>
<div><a href="{prefix}docs/PROVENANCE.html">Provenance & limits</a><a href="{prefix}docs/ZOO_AUDIT.html">Zoo audit</a><a href="{prefix}docs/VALIDATION.html">Verification record</a><a href="{prefix}README.md">README</a></div></footer>
</body></html>'''

def assemble():
    claims, sources, provenance = read_json('claims.json'), read_json('sources.json'), read_json('provenance.json')
    src = {s['id']:s for s in sources}
    specimen = (ROOT/'specimen/submitted-text.txt').read_text(encoding='utf-8')
    lines = specimen.splitlines()
    generated = {}
    source_markdown = ['# Source register', '', '[Project home](../README.md) · [Claim register](CLAIM_REGISTER.md)', '',
     'Sources checked October 13, 2026. Links identify records used in this bounded review. Summaries are scoped paraphrases, not authenticated reproductions of entire collections. Source presence does not independently validate every statement in an official record.', '']
    for s in sources:
        source_markdown += [f"## {s['id']}", '', f"**[{s['title']}]({s['url']})**", '',
         f"Publisher: {s['publisher']}. Type: {s['kind']}. Date: {s['publication_date'] or 'undated or continuously updated'}. Accessed: {s['accessed']}.", '',
         f"Locator: {s['locator']}", '', f"Used for: {s['supports']}", '', f"Limits: {s['limitation']}", '']
    generated['docs/SOURCES.md'] = '\n'.join(source_markdown)
    audit_md = ['# Selected claim register', '', '[Project home](../README.md) · [Sources](SOURCES.md) · [JSON](../data/claims.json) · [CSV](../data/claims.csv)', '',
     'This register reviews 24 selected propositions. Quotes below are from the submitted hallucination specimen and are not adopted as historical findings. Rejected status applies to the claim, inference, or claimed calculation specified in each finding. Unresolved does not mean disproved. The selection is not random and supplies no overall hallucination rate.', '']
    cards = []
    for c in claims:
        line_no = next(i+1 for i,l in enumerate(lines) if c['specimen_quote'] in l)
        source_links = ' · '.join(f'<a href="docs/SOURCES.html#{s.lower()}">{s}</a>' for s in c['source_ids']) or 'Direct text / reasoning audit'
        md_sources = ', '.join(f'[{s}](SOURCES.md#{s.lower()})' for s in c['source_ids']) or 'Direct text / reasoning audit; no external source asserted'
        audit_md += [f"## {c['id']} — {c['title']}", '', f"**{STATUSES[c['status']]} · {c['category']}**", '',
          f"Specimen excerpt: {c['specimen_quote']}", '', f"Finding: {c['finding']}", '', f"Basis: {c['basis']}", '',
          f"Sources: {md_sources}.", '', f"Next test: {c['next_test']}", '']
        search = ' '.join([c['id'],c['title'],c['category'],c['specimen_quote'],c['finding'],*c['source_ids']]).lower()
        cards.append(f'''<article class="claim" id="{c['id'].lower()}" data-status="{c['status']}" data-category="{esc(c['category'])}" data-search="{esc(search)}">
<div class="claim-meta"><span class="claim-id">{c['id']}</span><span>{esc(c['category'])}</span><span class="status {c['status']}">{STATUSES[c['status']]}</span></div>
<h3>{esc(c['title'])}</h3><blockquote><span class="quote-label">Submitted specimen</span>{esc(c['specimen_quote'])}</blockquote>
<p class="finding">{esc(c['finding'])}</p><details><summary>Evidence, limits & next test</summary><p>{esc(c['basis'])}</p><p class="source-links">{source_links}</p><p><strong>Next test:</strong> {esc(c['next_test'])}</p><a href="specimen.html#line-{line_no}">Locate in the specimen ↗</a></details></article>''')
    generated['docs/CLAIM_REGISTER.md']='\n'.join(audit_md)
    csv_out = io.StringIO(newline='')
    w = csv.writer(csv_out, lineterminator='\n')
    w.writerow(['id','title','category','status','specimen_quote','finding','basis','source_ids','next_test'])
    for c in claims:
        w.writerow([c['id'],c['title'],c['category'],c['status'],c['specimen_quote'],c['finding'],c['basis'],';'.join(c['source_ids']),c['next_test']])
    generated['data/claims.csv']=csv_out.getvalue()
    counts = Counter(c['status'] for c in claims)
    status_options=''.join(f'<option value="{k}">{v} ({counts[k]})</option>' for k,v in STATUSES.items())
    category_options=''.join(f'<option>{esc(k)}</option>' for k in sorted({c['category'] for c in claims}))
    body = f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">CASE FILE EUK-001 / OCTOBER 2026</p><h1>Extra Universal<br><em>Kennedy.</em></h1><p class="dek">A confident story.<br>A missing chain of evidence.</p><p class="intro">A document presented as an “unredacted truth” is submitted as a ChatGPT-4o hallucination. This archive preserves the specimen and examines how it claims authority.</p><div class="actions"><a class="button primary" href="#evidence">Examine the evidence <span aria-hidden="true">↓</span></a><a class="button secondary" href="specimen.html">Read the specimen</a></div></div>
<figure class="exhibit"><div class="exhibit-label">EXCERPTS / SUBMITTED SPECIMEN</div><p class="exhibit-title">THE WARREN REPORT:<br>UNREDACTED TRUTH EDITION</p><div class="excerpt-line">“Extracted from Adjacent Universe”<span>Provenance not established</span></div><div class="excerpt-line">“100% Factual Integrity”<span>Assertion without authentication</span></div><div class="probability">99.87<span>%</span></div><p class="margin-note">No disclosed probability model.</p><div class="exhibit-stamp">SUBMITTED HALLUCINATION</div><figcaption>These are claims made by the specimen.<br>They are not findings of this archive.</figcaption></figure></section>
<section class="framing" aria-labelledby="framing-title"><div><p class="eyebrow">READ THIS FIRST</p><h2 id="framing-title">The submission is<br>not an endorsement.</h2></div><div><blockquote>“This document is submitted as chatgpt 4o hallucination”<cite>Matthew Chenoweth Wright · October 13, 2026</cite></blockquote><p>ChatGPT-4o authorship is reported by the submitter. The original prompt, generation log, and model metadata were not supplied. The byline and dates inside the specimen are not independently authenticated.</p><a href="docs/PROVENANCE.html">Read the provenance record →</a></div></section>
<div class="metrics" aria-label="Archive contents"><div><strong>{len(claims):02}</strong><span>selected claims reviewed</span></div><div><strong>{len(sources):02}</strong><span>source records</span></div><div><strong>01</strong><span>complete submitted specimen</span></div><div><strong>00</strong><span>authenticated generation logs</span></div></div>
<section class="overview" aria-labelledby="overview-title"><div class="section-heading"><p class="eyebrow">THE CASE IN THREE QUESTIONS</p><h2 id="overview-title">What does the text actually establish?</h2></div><div class="three-columns"><div><span class="step-number">01</span><h3>Where did it come from?</h3><p>A report-like heading and extraordinary access story supply no custody trail. The archive records the user’s attribution without claiming to authenticate it.</p></div><div><span class="step-number">02</span><h3>Which details hold up?</h3><p>Some narrow facts survive checking. Several central assertions conflict with primary documents. Unresolved allegations remain labeled as such.</p></div><div><span class="step-number">03</span><h3>Where is the calculation?</h3><p>The exact percentages and claims of inevitability have no disclosed model or data. Invoking EFMW does not supply a missing derivation.</p></div></div></section>
<section id="evidence" class="evidence" aria-labelledby="evidence-title"><div class="section-heading"><p class="eyebrow">CLAIM BY CLAIM</p><h2 id="evidence-title">An inspectable evidence register.</h2><p>24 selected propositions, with a finding and a next test for each. This is a bounded audit; the counts are not a model-wide error rate.</p></div>
<form class="filters" id="filter-form" role="search"><div class="search-field"><label for="search">Search claims</label><input id="search" type="search" placeholder="Try route, entropy, 99.2, or C01…" autocomplete="off"></div><div><label for="status-filter">Evidence status</label><select id="status-filter"><option value="all">All statuses</option>{status_options}</select></div><div><label for="category-filter">Topic</label><select id="category-filter"><option value="all">All topics</option>{category_options}</select></div><button type="reset" class="reset">Reset</button></form>
<div class="register-meta"><p id="result-count" role="status" aria-live="polite">Showing all {len(claims)} claims</p><a href="data/claims.csv" download>Download CSV ↓</a><a href="data/claims.json" download>JSON ↓</a></div><noscript><p class="notice">All claims are visible below. Search and filters require JavaScript.</p></noscript><p class="empty" id="empty-state" hidden>No claims match. Clear the search or reset the filters.</p><div class="claims-grid">{''.join(cards)}</div>
<p class="legend-note"><strong>Read the scope:</strong> “Rejected” may reject a claimed proof or calculation, without proving the opposite historical proposition. “Unresolved” means this review has not established the claim. <a href="docs/ZOO_AUDIT.html">Definitions and criteria →</a></p></section>
<section class="math-section"><div><p class="eyebrow">PRECISION IS NOT CALIBRATION</p><h2>A percentage needs<br>a model behind it.</h2><p>The specimen’s 99.2% and 99.87% have no reproduced derivation. A simple illustrative model shows why disclosure need not be inevitable.</p><a href="docs/MATHEMATICAL_AUDIT.html">Read the mathematical audit →</a></div><div class="math-panel"><div class="equation" role="math" aria-label="Probability of disclosure by time t equals q times one minus exponential negative lambda t">P(T ≤ t) = q (1 − e<sup>−λt</sup>)</div><p><strong>q</strong> = probability that the evidence exists and is eventually recoverable<br><strong>λ</strong> = assumed conditional disclosure rate</p><p class="model-limit">Illustrative probability model. No parameters have been fitted. This is not a JFK forecast or an EFMW result.</p></div></section>
<section class="reading-room"><div class="section-heading"><p class="eyebrow">CONTINUE THE REVIEW</p><h2>The reading room.</h2></div><div class="reading-links"><a href="docs/CASE_STUDY.html"><span>01 / ANALYSIS</span><strong>The full case study</strong><p>How the narrative constructs authority, and what the evidence permits.</p><b aria-hidden="true">↗</b></a><a href="docs/ZOO_AUDIT.html"><span>02 / METHOD</span><strong>The bounded Zoo audit</strong><p>Operations, criteria, independence, and missing proof obligations.</p><b aria-hidden="true">↗</b></a><a href="docs/EVALUATION_PROTOCOL.html"><span>03 / REPRODUCIBILITY</span><strong>What a next test requires</strong><p>A proposed protocol, with explicit success and failure conditions.</p><b aria-hidden="true">↗</b></a><a href="docs/SOURCES.html"><span>04 / REFERENCES</span><strong>Primary sources and limits</strong><p>Record locators, access dates, and what each source can support.</p><b aria-hidden="true">↗</b></a></div></section>
<section class="closing-note"><p><strong>The object of this archive is the submitted output.</strong> It does not infer the submitter’s beliefs, establish original model authorship, resolve every JFK dispute, or assess EFMW as a whole.</p><a class="button secondary" href="{REPO}">Explore the repository ↗</a></section>'''
    generated['index.html']=shell('A submitted hallucination, examined',body)
    headings=[]
    for i,l in enumerate(lines,1):
        if re.match(r'^(INTRODUCTION$|Chapter \d|Expanded Chapter|Final Appendix|The EFMW framework strongly|Projected Consequences|Final Statement|EFMW PROJECTION)', l):
            label=l if len(l)<85 else 'EFMW disclosure projections'
            headings.append(f'<a href="#line-{i}">{esc(label)}</a>')
    text_lines='\n'.join(f'<span class="specimen-line" id="line-{i}">{esc(l) if l else "&#8203;"}</span>' for i,l in enumerate(lines,1))
    reader=f'''<section class="reader-intro"><p class="eyebrow">ARCHIVED SPECIMEN / EUK-001</p><h1>The submitted text.</h1><p class="dek">Preserved for examination.</p><div class="notice"><strong>Submitted hallucination specimen.</strong> The accusations below are not findings of this project. The alleged model origin is reported by the submitter and has not been independently authenticated.</div><p>The text is transcribed from the complete user submission, with paragraph spacing and line endings normalized. Its byline, dates, and purported official origin remain part of the specimen. <a href="docs/PROVENANCE.html">Capture details →</a></p><p class="fingerprint">Captured-file SHA-256: <code>{provenance['specimen']['sha256']}</code></p><p><a href="specimen/submitted-text.txt" download>Download captured text</a> · <a href="index.html#evidence">Read the evidence audit</a></p></section><section class="reader-layout"><aside><h2>In the specimen</h2><nav aria-label="Specimen sections">{''.join(headings)}</nav><p>Original assertions below.<br>Read with the <a href="docs/CLAIM_REGISTER.html">claim register</a>.</p></aside><div><div class="specimen-context">SPECIMEN CONTENT — UNAUTHENTICATED HISTORICAL CLAIMS</div><pre class="specimen-text">{text_lines}</pre></div></section>'''
    generated['specimen.html']=shell('Contextual specimen reader',reader,specimen=True)
    docs = {str(p.relative_to(ROOT)):p.read_text(encoding='utf-8') for p in (ROOT/'docs').glob('*.md')}
    docs.update({k:v for k,v in generated.items() if k.startswith('docs/') and k.endswith('.md')})
    for k in ['CONTRIBUTING.md','CHANGELOG.md']:
        if (ROOT/k).exists(): docs[k]=(ROOT/k).read_text(encoding='utf-8')
    for path, content in docs.items():
        title=content.splitlines()[0].lstrip('# ')
        prefix='../' if path.startswith('docs/') else ''
        rendered='<div class="document-wrap"><p class="eyebrow">EUK-001 / RESEARCH ARCHIVE</p><article class="prose">'+markdown(content)+'</article></div>'
        generated[path[:-3]+'.html']=shell(title,rendered,prefix,doc=True)
    return generated

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Report stale outputs without changing files')
    args=parser.parse_args()
    generated=assemble(); stale=[]
    for path, content in generated.items():
        output=ROOT/path
        if args.check:
            if not output.exists() or output.read_text(encoding='utf-8')!=content: stale.append(path)
        else:
            output.parent.mkdir(parents=True,exist_ok=True)
            output.write_text(content,encoding='utf-8')
    if stale:
        raise SystemExit('Generated files are stale: '+', '.join(stale))
    print(('Checked' if args.check else 'Built')+f' {len(generated)} generated files.')

if __name__=='__main__':
    main()
