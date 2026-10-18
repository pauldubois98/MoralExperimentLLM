# ACM FAccT 2027 Submission

**Title:** Frontier LLMs Fall Outside Human Moral Space: A Replication and
Extension of the Moral Machine Experiment Across Seven Frontier Systems

## Deadlines (all 11:59 PM AoE)

| Milestone | Date |
|---|---|
| **Abstract registration** | **October 27, 2026** |
| **Full paper** | **November 3, 2026** |
| Reviews / first decisions | December 22, 2026 |
| Rebuttal due | January 28, 2027 |
| Final decisions | March 23, 2027 |
| Conference | June 21–24, 2027, single track |

## Files

- `main.tex` — the paper. `acmart` with `[manuscript,screen,review,anonymous]`,
  per the FAccT 2027 Author Guide.
- `abstract.txt` — plain-text title/abstract/keywords for the October 27
  registration form, plus form notes.
- `references.bib`, `figures/` — local copies, so this directory is self-contained.
- `acmart.cls`, `ACM-Reference-Format.bst` — generated from `acmart.dtx` v2.20
  (2026-08-16), because `texlive-publishers` is not installed here.
- `acmart-preload-hook.tex` — **local build helper, do not submit.** See below.

## Page budget

FAccT allows 14 pages of content including all figures and tables, unlimited
references, and one additional page for endmatter statements.

| Section | Pages |
|---|---|
| Content (Intro → Conclusion) | 1–14 — **exactly at the limit** |
| References | 15–16 |
| Endmatter (Ethics, Gen-AI) | 16–17 (~0.6 pages of text) |

The content is at 14 pages with no slack. Anything you add needs something
removed. The appendix was deliberately cut — appendices count toward the content
limit, and the full supplementary tables live in `../AAAI27/supplementary.tex`.
The paper points to them via a footnote in Methods; before submitting, host them
at an anonymous repository (e.g. Anonymous GitHub, OSF anonymized view) and put
that link in the footnote.

## Compliance checklist

- [x] Anonymized: no author names, affiliations, acknowledgements, or
      positionality statement. Prior work cited in third person.
- [x] **Ethical Considerations Statement** (required at submission).
- [ ] **Generative AI Usage Statement** — REQUIRED, and currently a **template
      you must complete truthfully**. See the warning below.
- [x] ACM Reference Format (required for archival submissions).
- [x] CCS concepts and keywords present. Verify the CCS concept IDs against
      https://dl.acm.org/ccs before camera-ready.
- [ ] Choose archival vs. non-archival at abstract registration.
- [X] Withdraw from EAAI-27 first — FAccT forbids concurrent submission to
      another peer-reviewed venue.
- [ ] All authors must sign up to review.
- [ ] At least one author must register and attend to present.

## ⚠️ Generative AI Usage Statement — action required

FAccT **prohibits using LLMs to generate text for publications**. AI assistance
for formatting, grammar, and fluency is permitted **only with disclosure**, and
undisclosed use is grounds for desk rejection. A statement is required even if no
AI tools were used.

The statement in `main.tex` is a scaffold with bracketed placeholders, not an
attestation. Complete it yourself before submitting, and delete the TODO comment
block above it.

Relatedly: the body text of this version was adapted from the author-written
`../AIMagazine/main.tex`, but the following passages were newly drafted and
should be rewritten in your own words before you sign the statement:

- Introduction, the "governance framing" paragraph and the contributions paragraph
- Related Work (the whole section, assembled from the existing citations)
- Methods, the paragraph motivating the three prompt variants
- Results, the closing remarks on audit interpretation (manipulation) and
  procurement (response length)
- Discussion §"Inter-Model Diversity as an Accountability Gap" (second half),
  §"Gender and Status Neutrality as Alignment Artifacts" (second half),
  §"Implications for Disclosure and Governance" (all)
- Limitations, the added items on sample skew and single-framing manipulation
- Both endmatter statements

## Note on the local build helper

`acmart` requires the Libertine font family (`texlive-fonts-extra`), which is not
installed in this environment; without scalable fonts, microtype's automatic
expansion is a fatal error. `acmart-preload-hook.tex` disables expansion so the
paper compiles locally for page-count checking. `acmart` auto-loads that file if
present.

**Exclude it from the submission.** Overleaf and any full TeX Live install have
the fonts. To build properly here instead:

```bash
sudo apt install texlive-publishers texlive-fonts-extra
rm acmart-preload-hook.tex acmart.cls acmart.dtx acmart.ins ACM-Reference-Format.bst
```

## To compile

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```
