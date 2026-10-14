- Website : https://qualcoder.org/
- Software (source code) : https://github.com/ccbogel/QualCoder

Legacy English and French help URLs are kept working for already-released apps using
Zensical's built-in redirects in `zensical.toml`. Add future renamed or moved
pages to `[project.plugins.redirects.redirect_maps]`, using paths relative to
`docs`. Keep these mappings when updating the documentation.

The old English and French `/doc/<lang>/5.3.-Reports/` URLs redirect to
`docs/doc/<lang>/5.3.-legacy-reports-landing.md`, which links to both Analysis
and Reports, since older apps use the same URL for both sections. These legacy
landing pages are intentionally omitted from the navigation.
