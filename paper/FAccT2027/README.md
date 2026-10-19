# ACM FAccT 2027 Submission

**Title:** LLMs Driven Outside Human Moral Space: Extension of the Moral Machine
Experiment

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
| Content (Intro → Conclusion) | 1–13 — about one page under the limit |
| References | 13–14 |
| Endmatter (Ethics, Gen-AI) | 14–15 |

Related Work is folded into the Introduction. These counts come from the local
build without Libertine fonts. Recheck the page count on Overleaf or a full TeX
Live install before submitting. The appendix was deliberately cut — appendices count toward the content
limit, and the full supplementary tables live in `../AAAI27/supplementary.tex`.
The paper points to them via a footnote in Methods; before submitting, host them
at an anonymous repository (e.g. Anonymous GitHub, OSF anonymized view) and put
that link in the footnote.

## Compliance checklist

- [x] Anonymized: no author names, affiliations, acknowledgements, or
      positionality statement. Prior work cited in third person.
- [x] **Ethical Considerations Statement** (required at submission).
- [ ] **Generative AI Usage Statement** — REQUIRED. The draft has `[AUTHOR: ...]`
      fields you must complete truthfully. See the section below.
- [x] ACM Reference Format (required for archival submissions).
- [x] CCS concepts and keywords present. Verify the CCS concept IDs against
      https://dl.acm.org/ccs before camera-ready.
- [ ] Choose archival vs. non-archival at abstract registration.
- [X] Withdraw from EAAI-27 first — FAccT forbids concurrent submission to
      another peer-reviewed venue.
- [ ] All authors must sign up to review.
- [ ] At least one author must register and attend to present.

## ⚠️ Generative AI Usage Statement — action required

The FAccT 2027 Author Guide allows generative AI to be used substantively in
shaping or creating content, provided that use is disclosed with the model
version and the nature of the task. Spelling and grammar help must also be
listed. Undisclosed use is grounds for desk rejection. Every paper needs a
statement, including papers that used no AI tools.

The statement in `main.tex` is a draft, not an attestation. It records:

- **Revision to the current title and framing** (October 2026, Claude Opus 5.5
  via Claude Code). This touched every section, the endmatter excepted.
- **Earlier drafting**, for which you need to fill in the tool and version:
  LaTeX/template preparation, plus these passages, which were newly drafted
  rather than adapted from the author-written `../AIMagazine/main.tex`:
  - Introduction: the governance/accountability paragraph and the
    contributions paragraph
  - Related Work: the whole section
  - Methods: the paragraph motivating the three prompt variants
  - Results: the closing remarks on audit interpretation (manipulation) and
    procurement (response length)
  - Discussion: §5.2 (second half), §5.3 (second half), and §5.5 (all)
  - Limitations: the items on sample skew and single-framing manipulation
  - Both endmatter statements

Fill in the `[AUTHOR: ...]` fields, check that the statement is accurate, and
delete the TODO comment block above it.

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
