# arXiv Preprint

**Title:** Frontier LLMs Fall Outside Human Moral Space: A Replication and
Extension of the Moral Machine Experiment
**Author:** Paul Dubois (PRF Development)

Self-contained preprint version. Unlike the conference variants, this one is
de-anonymized, single-column, has no page limit, and merges the full-length body
with the complete supplementary appendices (A–E) in a single PDF.

## Composition

- **Body** — full-length text from `../AIMagazine/main.tex` (long abstract,
  complete Discussion, 11 figures).
- **Appendices A–E** — from `../AAAI27/supplementary.tex`, typeset in landscape
  via `pdflscape` because several tables are too wide for portrait.
- **Title** — the AAAI-27 title, which is the most recent.

Note: the Methods section's Gemini 3 Pro exclusion count was corrected from
"15 safety-filter parse failures" to the actual 34 (13 standard, 17 emphasis,
4 manipulation), which is what Tables A0 and A3 report. The AIMagazine and
AIES versions still carry the stale figure.

## To compile

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Everything needed is in this directory — `figures/` and `references.bib` are
local copies, not `../..` references, so the directory can be tarballed and
uploaded as-is.

## arXiv submission

**Suggested categories:**
- Primary: `cs.CY` (Computers and Society)
- Cross-list: `cs.AI`, `cs.CL`

**Package for upload:**

```bash
tar czf arxiv-submission.tar.gz main.tex main.bbl references.bib figures/
```

Include `main.bbl` — arXiv does not run BibTeX, it compiles the `.bbl` directly.
Do not include `.aux`, `.log`, `.blg`, or `main.pdf`.

**Checklist:**
- License: CC BY 4.0 recommended for maximum reuse (choose at submission; it
  cannot be downgraded later).
- Abstract must be pasted as plain text in the web form — strip LaTeX markup
  and keep it under 1,920 characters.
- No concurrent-submission conflict: arXiv is a preprint server, not a refereed
  venue, so posting here does not preclude a later conference or journal
  submission. Withdraw from EAAI-27 first regardless.
