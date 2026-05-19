# AAAI-27 Submission

**Venue:** 27th AAAI Conference on Artificial Intelligence  
**Dates:** February 16–23, 2027, Montréal, Canada  
**Deadlines:** Abstract July 21 / Full paper July 28, 2026

## Formatting requirements

- **Page limit:** 7 pages (content + figures) + unlimited references
- **Format:** 2-column AAAI style, double-blind anonymous
- **Template:** AAAI-2027 Author Kit (expected at https://aaai.org/authorkit27/ before July 2026; use aaai26 kit as placeholder)
- **Submission:** PDF

## Key constraints applied to article.md

- Author name removed (double-blind)
- Paper trimmed to fit 7-page target: manipulation and response-length sections condensed; some discussion points merged
- Core results (AMCE profiles, PCA map, prompt sensitivity) retained in full
- Suitable tracks: AI Alignment, AI for Social Impact, Multiagent Systems

## To compile

```bash
cd paper/AAAI27
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The local `aaai2026.sty` and `aaai2026.bst` are minimal stubs sufficient for proofing.
Once available, will need to replace them with the official AAAI-2027 Author Kit (`aaai27.sty` / `aaai27.bst` available at https://aaai.org/authorkit27/).
