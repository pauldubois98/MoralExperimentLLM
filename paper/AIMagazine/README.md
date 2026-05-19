# AI Magazine Submission

**Journal:** AI Magazine (Wiley / AAAI)
**ISSN:** 2371-9621
**URL:** https://onlinelibrary.wiley.com/journal/23719621

## Formatting requirements applied

- **Format:** Single-column, 11pt Times Roman, 1-inch margins, single-spaced
- **Abstract:** 250–350 words (expanded from conference version)
- **Citations:** Author-year style, e.g. (Awad et al. 2018), via `natbib` + `plainnat`
- **References:** Alphabetical by primary author surname; DOIs included
- **Language:** American English, active voice preferred
- **Acknowledgments:** Three sentences maximum
- **Author bio:** 3–5 sentences
- **Figures:** Inline at appropriate points, max 8×10 inches
- **Tables:** Full AMCE data in Appendix
- **Acronyms:** Five per article limit observed

Note: AI Magazine accepts Word/RTF/PDF; no official LaTeX template is provided.
This LaTeX source produces a submission-ready PDF.

## To compile

```bash
cd paper/AIMagazine
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
