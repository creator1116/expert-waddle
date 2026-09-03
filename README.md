# Expert Waddle — Static Wiki

This repository now contains a static, client-side wiki that reads its content from data/content.json. The Flask scaffold was removed in favor of a static site suitable for Cloudflare Pages or GitHub Pages.

How it works
- index.html is a small single-page app that fetches /data/content.json and renders collections and links in the browser.
- To add or update content, edit data/content.json (create a PR or push a commit). This is the canonical source.
- Deploy this repository to Cloudflare Pages (or another static host). No build step required.

Cloudflare Pages setup (recommended)
- Create a new Pages project and connect it to this repo and branch (e.g., feature/wiki-organization or main).
- Build settings: Framework preset = "None" (Static HTML). Leave the build command empty.
- Output directory: / (root)
- Save & deploy. Pages will serve index.html and the static assets.

Notes
- This is a read-only static site. "Editing" the wiki is done by editing data/content.json and merging commits.
- If you want a simple UI for editing in the browser, we can add a Cloudflare Worker or Pages Functions backed by a small API, or add a NetlifyCMS / Statically-hosted editor that commits to the repo.

Files of interest
- index.html — main single-page app
- static/ — CSS and JS
- data/content.json — canonical content (collections & links)

