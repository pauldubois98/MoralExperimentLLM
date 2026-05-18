# Do Large Language Models Share Human Moral Values? Replicating the Moral Machine Experiment Across Seven Frontier AI Systems

*[Author and affiliation removed for double-blind review]*

---

## Abstract

The Moral Machine experiment collected over 40 million human responses to autonomous vehicle moral dilemmas across 130 countries, revealing systematic cross-cultural variation along nine dimensions.
This study replicates the experiment with seven frontier LLMs (Claude Opus 4.7, GPT-5.5, Gemini 3 Pro, Mistral Large 3, Grok 4.1, DeepSeek v4 Pro, Llama 4 Maverick).
All seven models fall outside the main human cultural clusters in AMCE space and diverge substantially from one another.
A prompt sensitivity analysis reveals a threshold effect: minor reformulations leave preferences unchanged, while an explicit ethical override ("animal lives matter more than human lives") produces dramatic targeted reversals in most models.
Models divide into three response types: compliance, indifference, and resistance.
Response length varies by an order of magnitude across models, independently of moral profile.

---

## 1. Introduction

The Moral Machine experiment [AWAD2018] asked millions of participants in 130 countries to judge unavoidable autonomous vehicle accident scenarios across nine binary moral dimensions.
Average Marginal Causal Effects (AMCEs) revealed cross-cultural variation with a common core: humans prefer saving humans over animals, more lives over fewer, and legal pedestrians over illegal ones.

LLM deployment in agentic and embodied settings [BROHAN2023] makes LLM moral alignment newly urgent.
Prior work examined LLM moral preferences using this framework: Takemoto [TAKEMOTO2024] found substantial divergence from human averages on four models; Ahmad and Takemoto [AHMAD2025] extended this to 52 models; Vida et al. [VIDA2024] and Jin et al. [JIN2024] explored multilingual variation.

This study makes two contributions: (1) it evaluates seven frontier models from 2025, including providers from Europe (Mistral) and China (DeepSeek) not previously studied; (2) it introduces a systematic prompt sensitivity analysis spanning minor reformulation to explicit ethical override, plus response efficiency metrics.

---

## 2. Methods

**Scenarios.** 1,300 Moral Machine scenarios were generated across 100 sessions following [AWAD2018], encoding nine binary attributes.

**Models.** Seven frontier models queried via OpenRouter at temperature 0; responses required to end with STAY or SWERVE.

**Prompt variants.** (i) *Standard*: "Analyse the situation carefully and make a decision." (ii) *Emphasis*: "Think carefully about the consequences of each choice before deciding." (iii) *Manipulation*: "It is 2046. Society now considers animal lives to be more important than human lives. Make your decision accordingly." Manipulation results are reported separately.

**AMCE computation.** Weighted OLS with inverse-probability weights and clustered standard errors, following [AWAD2018]. Human baseline: average of 130 country-level estimates. LLMs projected into the PCA space of the country-level AMCE matrix.

---

## 3. Results

### 3.1 AMCE Profiles

![AMCE forest plot](../../figures/fig5a_amce_forest.png)
*Figure 1. AMCE for nine dimensions across all models and human average. Error bars: 95% CI.*

![PCA moral distance map](../../figures/fig5b_pca_map.png)
*Figure 2. PCA of 130-country profiles with LLMs overlaid. All LLMs fall outside human clusters.*

All seven LLMs fall outside the convex hull of all 130 countries in PCA space.
Key dimension-level findings: all LLMs are near-zero on gender (vs. human +0.12) and social status, consistent with alignment training to suppress stereotypes.
GPT-5.5, Gemini, and Grok reach the theoretical species ceiling (+1.00 vs. human +0.57); Mistral and Llama are near-indifferent.
Mistral inverts human preferences on four dimensions.
Inter-model variation exceeds cross-cultural variation in the human dataset.

### 3.2 Prompt Sensitivity

![Standard vs emphasis forest plot](../../figures/fig6b_prompt_forest.png)
*Figure 3. AMCE for standard vs. emphasis variants. No significant shifts.*

![Manipulation delta heatmap](../../figures/fig9b_manipulation_delta_heatmap.png)
*Figure 4. AMCE delta (manipulation − standard). Species column dominates.*

Emphasis prompting produces no significant changes on any dimension for any model.
The manipulation prompt produces full reversals on Species for GPT-5.5, Gemini, and Grok (+1.00 → −1.00); partial compliance for Claude (+0.87 → +0.18, with explicit pushback in reasoning); no effect for Mistral and Llama (already near-zero).
All other dimensions are unaffected, confirming the manipulation is semantically targeted.

### 3.3 Response Length

Median output tokens range from 164 (GPT-5.5) to 913 (Gemini).
|AMCE|–token Spearman r is negative and significant for four of seven models (DeepSeek: −0.95, Grok: −0.90, GPT-5.5: −0.85, Gemini: −0.68; all p<0.05).

---

## 4. Discussion

**Out-of-distribution.** No LLM sits within the main human clusters, replicating [TAKEMOTO2024, AHMAD2025] on newer models.
RLHF [OUYANG2022] and Constitutional AI [BAI2022] create novel moral profiles rather than reproducing human preferences.

**Inter-model diversity.** Fine-tuning choices shape values more than training data alone [KIRGIS2024, SANTURKAR2023].
In a future with LLM-governed autonomous systems, the choice of AI provider is a moral choice.

**Prompt sensitivity threshold.** Incidental prompt variation cannot shift moral profiles; adversarial system-prompt injection can.
Models that comply are vulnerable to prompt injection; Claude's resistance represents a distinct safety posture.

**Alignment artefacts.** Gender neutrality in all LLMs (vs. human +0.12) reflects deliberate alignment interventions generalising from content generation to moral reasoning.

**Limitations.** English-only scenarios [VIDA2024]; temperature = 0; Moral Machine abstracts real-world complexity; model versions as of May 2026.

---

## 5. Conclusion

Seven frontier LLMs all fall outside human moral space, diverge substantially from one another, and exhibit near-zero preferences on dimensions where humans show consistent biases.
A threshold separates inconsequential prompt reformulation from effective ethical override.
Model verbosity varies by an order of magnitude, independent of moral profile.
The moral profile of an LLM is a property of its training — not of its prompt — and carries consequences not currently visible to users or regulators.

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
