# FAccT 2027 Submission

**Venue:** ACM Conference on Fairness, Accountability, and Transparency  
**Dates:** 2027 (location TBA)  
**Deadlines:** ~January 2027 (FAccT 2026 was Jan 13, 2026)

## Formatting requirements

- **Page limit:** 14 pages (content) + 1 optional ethics/endmatter page + unlimited references
- **Format:** ACM LaTeX 2-column (manuscript style for review), double-blind anonymous
- **Template:** ACM TAPS — https://www.acm.org/publications/proceedings-template  
  Overleaf: https://www.overleaf.com/latex/templates/acm-conference-proceedings-primary-article-template/wbvnghjbzwpc  
  LaTeX: `\documentclass[manuscript,screen,review]{acmart}`
- **References:** ACM Reference Format (numbered [1], [2], ...)
- **Generative AI statement:** Required in endmatter

## Key constraints applied to article.md

- Author name removed (double-blind)
- References renumbered to ACM [n] format
- Generative AI usage statement added
- Framing emphasised toward accountability/fairness angle (deployment implications)
- 14 pages is generous — full content retained with expanded discussion

## To compile

1. Get ACM LaTeX template from the Overleaf link above
2. Use `acmart` class with `manuscript` option for review
3. Add `\acmConference{FAccT '27}{...}` header
4. Convert references to `\bibitem` entries in ACM format
