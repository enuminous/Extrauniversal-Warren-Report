# Release verification record

[Project home](../README.md) · [Provenance](PROVENANCE.md) · [Setup](SETUP.md)

Release: 1.0.0. Date: October 13, 2026.

## Checks supplied with the project

`scripts/verify.py` checks the specimen’s recorded checksum, byte count, opening and footer; selected quotation correspondence; unique claim and source IDs; valid evidence statuses; source references; local HTML links and fragments; Markdown file targets; Python syntax; and exact regeneration of the site.

`scripts/package.py` runs those checks before packaging, writes SHA-256 digests, and checks ZIP CRC integrity. `node --check assets/app.js` checks JavaScript syntax. The CI workflow repeats structural and syntax checks when run on GitHub.

## Scope and limits

The release was checked using those local structural, regeneration, syntax, and archive-integrity checks. Automated real-browser rendering and interaction checks were not available in the supported preview environment. Responsive styles, semantic landmarks, keyboard focus styles, labels, reduced-motion support, pre-rendered content, and a no-script reading path are implemented, but this is not a claim of a completed accessibility conformance audit.

Primary-source links and content were inspected during the evidence review. The verification script does not request every external URL or certify future link availability. It does not repeat historical investigations, perform ballistic experiments, authenticate original model authorship, or measure model-wide hallucination frequency.

Live GitHub publication, any CI run, and Pages hosting require separate remote verification. A prepared package or a passing local test is not a claim that a remote workflow or deployment succeeded.
