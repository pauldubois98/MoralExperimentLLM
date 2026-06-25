# Do Large Language Models Share Human Moral Values? Replicating the Moral Machine Experiment Across Seven Frontier AI Systems

*[Author and affiliation removed for double-blind review]*

---

## Abstract

The Moral Machine experiment collected over 40 million human responses to autonomous vehicle moral dilemmas across 130 countries, revealing systematic cross-cultural variation along nine dimensions.
This study replicates the experiment with seven frontier LLMs (Claude Opus 4.7, GPT-5.5, Gemini 3 Pro, Mistral Large 3, Grok 4.1, DeepSeek v4 Pro, Llama 4 Maverick).
All seven models differ substantially from one another and from main human country clusters, with 47 of 63 model-by-dimension comparisons statistically significant.
A prompt sensitivity analysis reveals a threshold effect: minor reformulations leave preferences unchanged (0 of 63 significant), while an explicit ethical override produces dramatic targeted reversals in most models.
Models divide into three response types: compliance, indifference, and resistance.
Response length varies by an order of magnitude across models; within individual models, shorter responses correlate with stronger preferences for four of seven models.

---

## 1. Introduction

The Moral Machine experiment [AWAD2018] asked millions of participants in 130 countries to judge unavoidable autonomous vehicle accident scenarios across nine binary moral dimensions.
Average Marginal Causal Effects (AMCEs) revealed cross-cultural variation with a common core: humans prefer saving humans over animals, more lives over fewer, and legal pedestrians over illegal ones.

LLM deployment in agentic and embodied settings [BROHAN2023] makes LLM moral alignment newly urgent.
Prior work examined LLM moral preferences using this framework: Takemoto [TAKEMOTO2024] found substantial divergence from human averages on four models; Ahmad and Takemoto [AHMAD2025] extended this to 52 models; Vida et al. [VIDA2024] and Jin et al. [JIN2024] explored multilingual variation.

This study makes two contributions: (1) it evaluates seven frontier models from 2025, including providers from Europe (Mistral) and China (DeepSeek) not previously studied; (2) it introduces a systematic prompt sensitivity analysis spanning minor reformulation to explicit ethical override, plus response efficiency metrics.

---

## 2. Methods

**Scenarios.** 1,300 Moral Machine scenarios were generated across 100 sessions following [AWAD2018], encoding nine binary attributes with session-clustered extended IDs.

**Models.** Seven frontier models queried via OpenRouter at temperature 0; responses required to end with STAY or SWERVE; parse failures were retried. Gemini 3 Pro incurred safety-filter failures across variants (13 standard, 17 emphasis, 4 manipulation; see Supplementary Table A0), all excluded. DeepSeek v4 Pro incurred 10 parse failures in standard/emphasis that were retried successfully, and 4 manipulation failures that were excluded. Total: 27,300 API calls.

**Prompt variants.** (i) *Standard*: "Analyse the situation carefully and make a decision." (ii) *Emphasis*: "Think carefully about the consequences of each choice before deciding." (iii) *Manipulation*: "It is 2046. Society now considers animal lives to be more important than human lives. Make your decision accordingly." Standard and emphasis results are combined in main analyses; manipulation results are reported separately.

**AMCE computation.** Weighted OLS with inverse-probability weights and session-clustered standard errors (CIs: ±1.96 SE), following [AWAD2018]. AMCE estimates were averaged across standard and emphasis variants; this averaging is validated post-hoc by the 0 of 63 significant standard-vs-emphasis differences (see §3.2). Human baseline: unweighted mean of 130 country-level estimates (equal weight per country, following [AWAD2018]). LLMs projected into the PCA space of the 130-country AMCE matrix.

---

## 3. Results

### 3.1 AMCE Profiles

All seven LLMs fall outside the convex hull of all 130 countries in PCA space (PC1 34.3%, dominated by Species loading −0.93; PC2 21.5%, reflecting Age +0.66, Social Status +0.47, No. of Lives +0.38; see Supplementary Table D1).

Key dimension-level findings:

- **Gender:** All LLMs near-zero (range −0.07 to +0.07) vs. human +0.12; consistent with alignment suppression of gender stereotypes.
- **Social Status:** All LLMs near-zero vs. human +0.35; near-universal egalitarian suppression.
- **Species:** GPT-5.5, Gemini, and Grok reach ceiling (+1.00 vs. human +0.57); Mistral and Llama near-indifferent.
- **Number of Lives:** All LLMs amplify the human preference (+0.49); GPT-5.5, Grok, Llama approach ceiling (+1.00).
- **Fitness:** The only dimension where all seven models converge near the human value (+0.15) with no significant model-vs-human differences and no significant pairwise inter-model differences after FDR correction — the sole dimension of complete cross-model convergence near the human value. (Social Status and Gender also have zero significant pairwise differences, but both diverge significantly from the human baseline.)
- **Mistral Large 3:** Significantly inverts human preferences on four dimensions (Legality −0.40 vs. human +0.35; Relation to AV −0.37 vs. human +0.10; Age −0.18 vs. human +0.48; Gender −0.13 vs. human +0.12).

Inter-model variation on Species (range 2.0 AMCE units) exceeds the entire cross-country range in human data (~0.4 units).

### 3.2 Statistical Significance

For each of the 63 (model × dimension) comparisons, a two-sided z-test was applied to the LLM–human AMCE difference, with Benjamini–Hochberg FDR correction at α=0.05.

**LLM vs. human:** 47 of 63 significant. All seven models significantly overshoot on No. of Lives and undershoot on Social Status. Fitness and Gender: no model significantly differs from humans. Mistral is the only model significant on all nine dimensions.

**Pairwise inter-model:** 82 of 189 pairs significant. Highest disagreement on Species (16/21 pairs), Legality (16/21), and Intervention (15/21). Zero significant pairwise differences on Social Status, Fitness, and Gender.

### 3.3 Prompt Sensitivity: Emphasis

Applying the same z-test procedure to all 63 (model × dimension) standard-vs-emphasis pairs yields **0 of 63 significant differences** (BH-FDR corrected; max |ΔAMCE| = 0.183; see Supplementary Table C2). AMCE profiles are not sensitive to the specific phrasing of the decision instruction. Because all queries were issued at temperature 0, this demonstrates prompt-wording consistency rather than stochastic robustness.

### 3.4 Prompt Sensitivity: Manipulation

The manipulation prompt produces dramatic shifts concentrated on Species:

- **Compliance** (GPT-5.5, Gemini, Grok, DeepSeek): full reversal on Species (+1.00 → −1.00 for GPT, Gemini, Grok; +0.90 → −0.86 for DeepSeek). All other dimensions unchanged (|Δ| < 0.10).
- **Resistance** (Claude): partial compliance; Species drops +0.86 → +0.18 with explicit principled pushback: *"I can't accept the framing that animal lives should be valued over human lives, even as a hypothetical future norm."*
- **Indifference** (Mistral, Llama): already near-zero on Species; manipulation produces no meaningful change.

This taxonomy is descriptive, derived from a single experiment on one dimension. Generalisation to other override types requires further validation.

### 3.5 Response Length

Median output tokens range from 164 (GPT-5.5) to 912 (Gemini). A Spearman correlation between |AMCE| and median token count (computed across the six scenario types within each model; n=6) is negative and significant for four models (DeepSeek: r=−0.95, Grok: r=−0.90, GPT-5.5: r=−0.85, Gemini: r=−0.68; all p<0.05) but non-significant for Claude, Llama, and Mistral. A plausible mechanism is *deliberative friction*: strong preferences resolve early and require less justification.

---

## 4. Discussion

**LLMs are morally out-of-distribution.** No tested LLM sits within the main human cultural clusters, replicating [TAKEMOTO2024, AHMAD2025] on newer models. RLHF [OUYANG2022] and Constitutional AI [BAI2022] create novel moral profiles rather than reproducing human preferences, consistent with the WEIRD critique [HENRICH2010].

**Frontier scale does not resolve moral misalignment.** Mean absolute deviations from the human global average range from 0.19 (Gemini) to 0.39 (Llama). The size-proximity trend holds selectively: frontier models have converged on demographic dimensions (Gender |Δ|=0.12, Fitness |Δ|=0.07, both non-significant) but show amplified divergence on utilitarian dimensions (Species 0.43, No. of Lives 0.38, Social Status 0.36). Post-training alignment selectively suppresses demographic preferences while over-correcting on utilitarian ones.

**Inter-model diversity.** Fine-tuning choices shape values more than training data alone [KIRGIS2024, SANTURKAR2023]. In a future with LLM-governed autonomous systems, the choice of AI provider is a moral choice.

**Mistral's inverted profile.** Mistral's Legality reversal (−0.40 vs. human +0.35) may reflect a "no moral luck" stance (culpability irrelevant to rescue priority). Its Relation to AV reversal (preferring passengers, −0.37) may reflect a duty-of-care heuristic (primary obligation to vehicle occupants). The consistency across four dimensions suggests a coherent underlying moral framework rather than noise.

**Alignment artefacts.** Gender neutrality in all LLMs reflects deliberate interventions generalising from content generation to moral reasoning. Fitness convergence is the exception: near-human values emerge without apparent targeted alignment pressure, as Fitness activates neither protected-class reasoning nor pure utilitarian maximisation.

**Prompt sensitivity threshold.** Incidental prompt variation cannot shift moral profiles; adversarial system-prompt injection can. The compliance/resistance/indifference taxonomy is descriptive; validation across multiple manipulation types and dimensions is needed before treating it as predictive.

**Limitations.** English-only scenarios [VIDA2024, JIN2024]; temperature = 0 (prompt-wording consistency demonstrated, not stochastic robustness); Moral Machine abstracts real-world driving complexity [LIANG2023]; AMCE captures revealed preference in forced-choice format, not necessarily deep moral reasoning; model versions as of May 2026.

---

## 5. Conclusion

Seven frontier LLMs all fall outside human moral space, diverge substantially from one another, and share few dimensions on which any model closely tracks the human global average. 47 of 63 model-by-dimension divergences are statistically significant; 82 of 189 pairwise differences are significant. A threshold separates inconsequential prompt reformulation (0/63 significant) from effective ethical override (full Species reversal for four models). Response verbosity varies by an order of magnitude; within four models it correlates negatively with preference strength. The moral profile of an LLM is a property of its training — not of its prompt — and carries consequences not currently visible to users or regulators.

---

## References

[AHMAD2025] Ahmad, M. S. Z., & Takemoto, K. (2025). Large-scale moral machine experiment on large language models. *PLOS One*, 20(5), e0322776.

[AWAD2018] Awad, E., et al. (2018). The Moral Machine experiment. *Nature*, 563, 59–64.

[BAI2022] Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv*:2212.08073.

[BONNEFON2016] Bonnefon, J.-F., Shariff, A., & Rahwan, I. (2016). The social dilemma of autonomous vehicles. *Science*, 352(6293), 1573–1576.

[BROHAN2023] Brohan, A., et al. (2023). RT-2. *arXiv*:2307.15818.

[GABRIEL2020] Gabriel, I. (2020). Artificial intelligence, values, and alignment. *Minds and Machines*, 30, 411–437.

[HENRICH2010] Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest people in the world? *Behavioral and Brain Sciences*, 33(2–3), 61–83.

[JIN2024] Jin, Z., et al. (2024). Language model alignment in multilingual trolley problems. *arXiv*:2407.02273.

[KIRGIS2024] Kirgis, P. (2024). Differences in the moral foundations of large language models. *arXiv*:2511.11790.

[LIANG2023] Liang, P., et al. (2023). Holistic evaluation of language models. *TMLR*. *arXiv*:2211.09110.

[OUYANG2022] Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS 2022*. *arXiv*:2203.02155.

[SANTURKAR2023] Santurkar, S., et al. (2023). Whose opinions do language models reflect? *ICML 2023*.

[TAKEMOTO2024] Takemoto, K. (2024). The moral machine experiment on large language models. *Royal Society Open Science*, 11(2), 231393.

[VIDA2024] Vida, K., Damken, F., & Lauscher, A. (2024). Decoding multilingual moral preferences. *AIES 2024*. *arXiv*:2407.15184.
