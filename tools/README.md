# tools

Generators for the profile and for every repository banner and README. One palette, one type system, one place to edit.

| file | what |
|:--|:--|
| `common.py` | Palette (obsidian ground, sage trio, ink), fonts, SVG helpers, animations. |
| `repos.py` | The single source of truth for every repo: title, tagline, description, topics, homepage, local path. |
| `banners.py` | Writes `assets/banner.svg` into each repo. |
| `readmes.py` | Writes each repo's `README.md` (and `INDEX.md` for Competitive-Programming). |
| `profile.py` | Writes the profile panels into `assets/` and a preview page into `$PREVIEW_DIR`. |
| `apply_metadata.py` | Pushes descriptions, topics and homepages to GitHub through the API. |

```bash
python3 tools/profile.py                 # regenerate the profile panels
python3 tools/banners.py && python3 tools/readmes.py   # regenerate every repo banner and README
python3 tools/apply_metadata.py          # repo metadata; PROFILE=1 also sets company/blog
```
