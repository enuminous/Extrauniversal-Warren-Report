# Extra Universal Kennedy

<!-- ENUMINOUS-UNIFIED-NAV:START -->
## Repository navigation

**eNuminous network:** [All public repositories](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md) · [EFMW](https://github.com/enuminous/EFMW) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [Frozen Lean](https://github.com/enuminous/Monolithic-102-Zoo-Lean4) · [Zoo](https://github.com/enuminous/Tortoise) · [Papers](https://github.com/enuminous/papers) · [Quantum geometry](https://github.com/enuminous/Base888-Quantum-Geometry)

**This project:** [Repository home](https://github.com/enuminous/Extrauniversal-Warren-Report) · [Subject index](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md#papers-publications-and-creative-work)

<details open>
<summary><strong>On this page</strong></summary>

- [What is here](#what-is-here)
- [Start reading](#start-reading)
- [GitHub and Pages](#github-and-pages)
- [Maintain the evidence record](#maintain-the-evidence-record)
- [Project map](#project-map)
- [Attribution and limits](#attribution-and-limits)


</details>

**Related repositories:** [Harlequinn](https://github.com/enuminous/Harlequinn) · [I-Have-Guts](https://github.com/enuminous/I-Have-Guts) · [Alchemy-of-Emergence](https://github.com/enuminous/Alchemy-of-Emergence) · [Wrights-Law](https://github.com/enuminous/Wrights-Law) · [papers](https://github.com/enuminous/papers) · [EFMW](https://github.com/enuminous/EFMW)

> **Evidence boundary:** A link between projects is navigation, not an assertion of proven equivalence, experimental validation, or shared authorship. See each repository’s own status and review notes.
<!-- ENUMINOUS-UNIFIED-NAV:END -->


**A submitted AI hallucination specimen, preserved with a source-linked evidence audit.**

[Repository](https://github.com/enuminous/Extrauniversal-Warren-Report) · [Project page source](index.html) · [Read the case study](docs/CASE_STUDY.md) · [Inspect 24 claims](docs/CLAIM_REGISTER.md) · [Review provenance](docs/PROVENANCE.md) · [Sources](docs/SOURCES.md)

Matthew Chenoweth Wright submitted the text titled *The Warren Report: Unredacted Truth Edition* and clarified on October 13, 2026: **“This document is submitted as chatgpt 4o hallucination”.** This repository documents that submission. Possession or submission of the text does not establish endorsement of its accusations.

The attribution to **ChatGPT-4o is reported by the submitter**. An original generation transcript, original prompt, model identifier, and generation settings were not supplied. This project does not authenticate the model attribution or claim to reproduce the original generation.

## What is here

- A contextual reader and complete plain-text transcription of the submitted specimen.
- A responsive, searchable static website suitable for GitHub Pages and local use.
- A register of **24 selected claims**, with scoped findings, evidence status, source identifiers, and next tests.
- **14 source records**, including primary documents, investigations, scientific work, archival updates, and GitHub setup documentation.
- A case study, a bounded Zoo-method audit, mathematical critique, provenance record, and evaluation protocol.
- Rebuild and verification scripts using only Python’s standard library, plus a GitHub Actions check.

The website renders its evidence records before JavaScript runs. Search and filtering enhance the page; the content remains readable with scripts disabled. It uses local assets, no analytics, and no remote fonts.

## Start reading

1. Open **`index.html`** after extracting the ZIP.
2. Read the evidence framing, then inspect individual claims and their sources.
3. Open **`specimen.html`** to read the submitted document with its context attached.

The case concerns unsupported factual presentation: purported extraordinary access, unsourced historical specificity, unsupported percentages, and claims of mathematical inevitability. It does not settle every JFK dispute, validate or invalidate EFMW as a whole, or establish a model-wide error rate.

## GitHub and Pages

Authorized repository: **[enuminous/Extrauniversal-Warren-Report](https://github.com/enuminous/Extrauniversal-Warren-Report)**. Display title and ZIP name: **Extra Universal Kennedy**.

1. Open the named repository, or create your own copy if reusing this package.
2. For a manual upload, upload the **contents inside** the extracted `Extra-Universal-Kennedy` folder, so `README.md` and `index.html` are at the repository root.
3. For a website, select **Settings → Pages → Deploy from a branch → main → / (root) → Save**. The included `.nojekyll` file keeps the site static.
4. Use the URL GitHub returns after the deployment completes.

The ZIP is a portable snapshot of the project. Repository publication and Pages hosting are separate; use GitHub’s deployment result to determine whether Pages is enabled. Detailed instructions and the official documentation link are in [SETUP.md](docs/SETUP.md).

## Maintain the evidence record

Python 3.10 or newer is sufficient; there are no pip dependencies.

```bash
python3 scripts/build_site.py
python3 scripts/verify.py
```

Edit `data/claims.json` and `data/sources.json` for evidence changes. The builder updates the website, claim register, source bibliography, and CSV export. Change substantive judgments only with documented evidence and an explanation. Preserve `specimen/submitted-text.txt` as the frozen v1 capture; use a new version for any later source correction.

```bash
python3 scripts/package.py --output ../Extra-Universal-Kennedy.zip
```

The packager verifies the project and includes a SHA-256 manifest. A matching checksum establishes package integrity, not historical authenticity or model authorship.

## Project map

| File or folder | Purpose |
|---|---|
| `index.html`, `specimen.html`, `assets/` | Static project website and contextual specimen reader |
| `specimen/` | Preserved text and capture notice |
| `data/claims.json`, `data/claims.csv` | Machine-readable selected claim register |
| `data/sources.json` | Source records with scope and limitations |
| `data/provenance.json` | Attribution, dates, capture method, specimen checksum |
| `docs/CASE_STUDY.md` | Full interpretive case study |
| `docs/ZOO_AUDIT.md` | Bounded operations, criteria, and proof obligations |
| `docs/MATHEMATICAL_AUDIT.md` | Probability and inevitability checks |
| `docs/EVALUATION_PROTOCOL.md` | Prospective replication and scoring design |
| `docs/VALIDATION.md` | What was and was not verified for this release |
| `scripts/` | Deterministic rendering, validation, and packaging |

## Attribution and limits

Case submitter: **Matthew Chenoweth Wright**. Archive and analysis prepared with AI assistance on **October 13, 2026**. The internal February 10, 2025 publication date and August 19, 2025 export date belong to the specimen and have not been independently authenticated.

All findings are reviewable judgments with a stated scope. An official report is evidence of what that report concluded; it is not automatically the final word on every historical question. No repository-wide reuse license has been selected; see [LICENSE](LICENSE).

[Contribution rules](CONTRIBUTING.md) · [Release notes](CHANGELOG.md) · [Citation metadata](CITATION.cff)
