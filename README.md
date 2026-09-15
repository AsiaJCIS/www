# AsiaJCIS website

Source of <https://asiajcis.github.io/www/> — the umbrella site of the Asia Joint Conference on Information Security (AsiaJCIS, formerly JWIS).
Built with [MkDocs](https://www.mkdocs.org/) from `docs/` and deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.

- `docs/2027/` — the current conference
- `docs/index.md` — list of all past conferences (2006–) with links to the archived sites
- `docs/archive/<year>-<country>/` — static snapshots of every past conference site

## What this repository deliberately does NOT contain

The archived sites are kept so that the history of the conference survives the original host sites going offline. To keep them safe to publish, the following are removed from every snapshot and must not be re-added:

1. **Conference photo galleries** (group photos, banquet/session snapshots). Venue and hotel images and speaker portraits from the original pages are kept.
2. **Analytics, tracking and third-party scripts** — Google Analytics/Tag Manager, Baidu Tongji, Facebook SDK, cookie-consent managers, Google Sites viewer scripts, etc. The pages must not load any external JavaScript. (Google Fonts and Google Maps iframes from the original pages are tolerated.)
3. **Links to the Internet Archive (`web.archive.org`) or archive.today.** Where a page or image could not be recovered, the link is unwrapped (text kept) or the element dropped; we do not send visitors to third-party archives.
4. **Bank account numbers** on registration pages — replaced with `(omitted in archive)`.
5. **E-mail addresses** (personal and secretariat) — replaced with `(email omitted in archive)`; `mailto:` links removed. Most of them are no longer valid anyway.
6. **Internal tooling and fetch metadata** — the mirroring scripts, procedure notes and per-year source manifests live outside this repository.

Papers, programs, calls for papers and invited-talk material from the original sites **are** kept: for the JWIS years (2006–2011) they are the only record, since no formal proceedings were published.

The archive is indexable by search engines (`docs/robots.txt` allows everything) so that past programs and papers remain findable and citable.

## Contributing

Changes are committed to `main` by the maintainers only, after review. AI coding agents used for maintenance must not commit or push (see `AGENTS.md`).

## Corrections and takedown

Found a problem with the site or the archive — a broken page, a wrong name, something that should not be public? **Please open an issue: <https://github.com/AsiaJCIS/www/issues>.** That is the primary channel; it keeps a public record of what was reported and what was done.

Each archived HTML file starts with a comment giving its source URL and, for reconstructed sites, the Internet Archive capture time, so you can point at exactly what you mean. Authors, former organizers and host institutions asking for a correction or removal will be handled the same way.
