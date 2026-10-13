# Use, rebuild, and publish

[Project home](../README.md) · [Verification record](VALIDATION.md)

## Open locally

Extract the ZIP and open `index.html`. All content, styles, icons, and scripts are local. The evidence register is pre-rendered; filtering uses JavaScript without a server or network request. External source links require a network connection.

## Repository destination

The authorized GitHub destination is [enuminous/Extrauniversal-Warren-Report](https://github.com/enuminous/Extrauniversal-Warren-Report). The project’s display title and ZIP name remain Extra Universal Kennedy.

If uploading manually, upload the contents inside the extracted project folder so `index.html` is at the root. Preserve the `assets`, `data`, `docs`, `scripts`, and `specimen` directories. Use Git for hidden files such as `.nojekyll` and `.github` if your file picker omits them.

## GitHub Pages

In the repository, choose **Settings → Pages → Deploy from a branch → main → / (root) → Save**. GitHub supplies the actual deployed URL. Repository publication and Pages deployment are separate actions; a repository link does not establish that Pages has been enabled.

The site uses relative paths so it works under a repository subpath. It has no npm build step. The `.nojekyll` file disables Jekyll processing. The included `verify.yml` workflow checks the package and does not deploy it.

Official source: [GitHub Pages publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), checked October 13, 2026.

## Rebuild

Requires Python 3.10 or newer. No third-party Python packages are needed.

```bash
python3 scripts/build_site.py
python3 scripts/verify.py
```

Optional JavaScript syntax check with Node.js:

```bash
node --check assets/app.js
```

The builder generates HTML versions of the Markdown documentation, the home page, specimen reader, source register, claim register, and CSV. Edit the Markdown or JSON inputs and rebuild rather than editing generated files directly.

## Package

```bash
python3 scripts/package.py --output ../Extra-Universal-Kennedy.zip
```

The ZIP contains one top-level `Extra-Universal-Kennedy` directory and a checksum manifest. The manifest verifies captured bytes. It is not proof of historical authenticity.

If modifying a tree extracted from a release ZIP, remove its old `SHA256SUMS.txt` before intentional edits, then regenerate the package to produce a new manifest. Preserve the original release archive if its integrity is important to the audit trail.
