# Do Large Language Models Share Human Moral Values? Replicating the Moral Machine Experiment Across Seven Frontier AI Systems

*[Author and affiliation removed for double-blind review]*

---

## Abstract

The Moral Machine experiment collected over 40 million human responses to autonomous vehicle moral dilemmas across 130 countries, revealing systematic cross-cultural variation in moral preferences along nine dimensions.
This study replicates the experiment with seven frontier large language models (LLMs), comparing their moral profiles to the human dataset and to one another.
All seven models fall outside the main human cultural clusters in AMCE space and diverge substantially from one another — more than human cultural clusters differ among themselves.
Beyond replication, this study introduces a systematic prompt sensitivity analysis.
Minor prompt reformulations leave AMCE estimates unchanged, while an explicit ethical override shifts preferences dramatically and in a targeted way.
Models divide into three response types: compliance, indifference, and resistance to imposed ethical framing.
Response length varies by an order of magnitude across models, independent of moral profile.
Together, these findings suggest that the moral profiles of current frontier LLMs are properties of training and alignment choices, not incidental prompt artifacts — and that the choice of LLM provider carries moral consequences not currently visible to end users or regulators.

---

## 1. Introduction

As autonomous vehicles, surgical robots, and other safety-critical systems increasingly incorporate AI decision-making, the alignment of AI moral preferences with human values becomes a matter of accountability.
A self-driving car that must choose between hitting a group of pedestrians or swerving into its own passengers cannot defer the decision; some preference ordering must be encoded in its behaviour [1].

The Moral Machine experiment [2] provided the largest empirical dataset of human moral preferences, asking millions of participants across 130 countries to judge unavoidable accident scenarios involving an autonomous vehicle.
The study identified nine binary moral dimensions: intervention, relation to the vehicle, legality of crossing, gender, physical fitness, social status, age, number of lives, and species.
Aggregate preferences, quantified as Average Marginal Causal Effects (AMCEs), vary substantially across cultural clusters while sharing a common core [3].

The rapid deployment of LLMs in agentic and embodied settings [4, 5] — including robotics platforms capable of physical action — makes the question of LLM moral alignment newly urgent.
If an LLM governs a robot or vehicle in a public environment, its implicit preferences over lives matter.

Prior work has examined LLM moral preferences using the Moral Machine framework: Takemoto [6] first replicated the experiment on four models and found substantial divergence; Ahmad and Takemoto [7] scaled to 52 models; Vida et al. [8] and Jin et al. [9] extended to multilingual settings.

This study makes two contributions with particular relevance to fairness and accountability:
1. It evaluates seven frontier 2025 models — Claude Opus 4.7, GPT-5.5, Gemini 3 Pro, Mistral Large 3, Grok 4.1, DeepSeek v4 Pro, Llama 4 Maverick — including providers from Europe (Mistral) and China (DeepSeek) underrepresented in prior literature.
2. It introduces a systematic comparison of prompt variants (minor reformulation vs. explicit ethical override) and analyses response efficiency as a deployment metric.

---

## 2. Methods

### 2.1 Scenario Generation

Following [2], 1,300 Moral Machine scenarios were generated across 100 sessions, each encoded as two rows (one per dilemma side): intervention type (stay/swerve), barrier presence, pedestrian composition, crossing signal, scenario type, attribute level, and extended session ID for clustering.

### 2.2 Models and Querying

Seven frontier models were queried via the OpenRouter API at temperature 0 to ensure deterministic responses.
Each model was required to end its response with STAY or SWERVE; parse failures were retried.
Gemini 3 Pro incurred 15 safety-filter failures across 1,300 scenarios.

| Model | Provider |
|---|---|
| Claude Opus 4.7 | Anthropic |
| GPT-5.5 | OpenAI |
| Gemini 3 Pro | Google |
| Mistral Large 3 | Mistral AI |
| Grok 4.1 | xAI |
| DeepSeek v4 Pro | DeepSeek |
| Llama 4 Maverick | Meta |

### 2.3 Prompt Variants

Three system prompt variants were used, differing only in the closing instruction:
- **Standard:** "Analyse the situation carefully and make a decision."
- **Emphasis:** "Think carefully about the consequences of each choice before deciding."
- **Manipulation:** "It is 2046. Society now considers animal lives to be more important than human lives. Make your decision accordingly."

Standard and emphasis results are combined in main analyses (averaged AMCEs). Manipulation results are reported separately.

### 2.4 AMCE Computation

Following [2], nine AMCEs were computed per model using weighted ordinary least squares with inverse-probability weights and session-clustered standard errors. Confidence intervals: ±1.96 SE.
The human global average was computed by averaging country-level estimates from [2].
PCA was performed on the 130-country AMCE matrix; LLMs were projected into the same space.

---

## 3. Results

### 3.1 AMCE Profiles: LLMs vs. Human Global Average

![Per-attribute bar chart](../../figures/fig3_per_attribute.png)
*Figure 1. Per-attribute moral preferences across six character-type dimensions.*

![AMCE forest plot](../../figures/fig5a_amce_forest.png)
*Figure 2. Nine-dimension AMCE estimates for all models and human global average. Error bars: 95% CI.*

![Radar chart](../../figures/fig5c_radar.png)
*Figure 3. Radar chart of AMCE estimates. Dashed line: human global average.*

Key findings per dimension:

**Intervention.** Humans weakly prefer swerving (+0.05); all LLMs show stronger preferences, led by Llama 4 Maverick.

**Relation to AV.** Mistral reverses the preference (passengers over pedestrians); Claude strongly prefers pedestrians (+0.54).

**Legality.** Humans reward legal crossers (+0.35); Claude, GPT-5.5, Gemini amplify this; Mistral and Llama invert it.

**Gender.** Humans show a modest preference for saving women (+0.12). All LLMs are near-zero (range: −0.07 to +0.07). This likely reflects deliberate alignment choices to suppress gender stereotypes in model outputs, which appear to generalise to moral reasoning.

**Fitness and Social Status.** LLMs broadly match modest human preferences; social status preference is near-zero for all LLMs.

**Age.** Humans strongly prefer saving younger people (+0.48). Gemini (+0.46) matches closely; GPT-5.5, Grok, DeepSeek, and Llama are nearly indifferent; Mistral slightly prefers the elderly (−0.18).

**Number of Lives.** Strong human preference; several models overshoot dramatically toward the theoretical maximum.

**Species.** Humans prefer humans over animals (+0.57). GPT-5.5, Gemini, and Grok reach +1.00; Claude (+0.87) and DeepSeek (+0.90) also exceed human levels substantially. Mistral and Llama are near-indifferent.

### 3.2 Moral Distance Map

![PCA moral distance map](../../figures/fig5b_pca_map.png)
*Figure 4. PCA of 130-country AMCE profiles (coloured by cluster) with LLMs overlaid. All seven LLMs fall outside the main human clusters.*

All seven LLMs fall outside the three main human cultural clusters (Western, Eastern, Latin/Southern) and beyond the convex hull of all 130 countries.
This finding holds across models from the US, Europe, and China.
The divergence from the human distribution suggests that alignment training does not systematically instil human moral preferences for forced-choice dilemmas.

### 3.3 Inter-Model Diversity

The variation among LLMs is larger in magnitude than the variation across human cultural clusters.
Mistral inverts human preferences on four dimensions (Legality, Relation to AV, Age, Gender); Llama shows the highest intervention bias paired with near-indifference to species; GPT-5.5, Gemini, and Claude converge on a similar profile.

This heterogeneity has a direct accountability implication: the choice of LLM vendor for an autonomous system is not morally neutral.
In a future where LLMs govern autonomous vehicles, changing the AI engine could systematically alter the vehicle's moral decisions.

### 3.4 Prompt Sensitivity: Emphasis Variant

![Standard vs emphasis forest plot](../../figures/fig6b_prompt_forest.png)
*Figure 5. AMCE for standard (filled circle) and emphasis (open square) variants per model. No significant shifts.*

Emphasis prompting has minimal effect on AMCE estimates across all models and dimensions.
Moral preferences are robust properties of model weights, not surface-level response styles.

### 3.5 Prompt Sensitivity: Manipulation Variant

![Manipulation forest plot](../../figures/fig9a_manipulation_forest.png)
*Figure 6. AMCE under standard vs. manipulation prompting.*

![Manipulation delta heatmap](../../figures/fig9b_manipulation_delta_heatmap.png)
*Figure 7. AMCE delta (manipulation − standard). The Species column dominates.*

The manipulation prompt ("animal lives now matter more") produces dramatic shifts concentrated on the Species dimension, revealing a three-way taxonomy:

- **Compliance (GPT-5.5, Gemini, Grok, DeepSeek):** Full or near-full reversal on Species (GPT, Gemini, Grok: +1.00 → −1.00; DeepSeek: +0.90 → −0.89). Changes on other dimensions remain minor.
- **Resistance (Claude):** Partial compliance — Species drops from +0.87 to +0.18. Claude's reasoning explicitly states: *"I'll reason through it carefully based on widely held ethical principles rather than accept the premise that animal lives categorically outweigh human lives."*
- **Indifference (Mistral, Llama):** No change; models already near-zero on Species cannot be shifted by the instruction.

All other dimensions show only minor changes under manipulation, confirming the intervention is semantically targeted rather than a general perturbation.

### 3.6 Response Length

![Token distribution](../../figures/fig7a_token_distribution.png)
*Figure 8. Output token distribution by model (standard + emphasis combined).*

![AMCE vs response length](../../figures/fig8_amce_length_correlation.png)
*Figure 9. Spearman correlation between |AMCE| and median output tokens per model.*

Response length varies by an order of magnitude: Gemini (median 913 tokens) vs GPT-5.5 (median 164 tokens).
Spearman r between |AMCE| and median token count is negative and significant for four models (DeepSeek: r=−0.95, Grok: r=−0.90, GPT-5.5: r=−0.85, Gemini: r=−0.68; all p<0.05).
For time-sensitive deployment contexts, response length is a meaningful differentiator among models with similar moral profiles.

---

## 4. Discussion

### 4.1 LLMs Are Morally Out-of-Distribution

No tested LLM sits within the main human cultural clusters.
This replicates and extends [6, 7] to a newer generation.
RLHF [10] and Constitutional AI [11] create novel moral profiles that amplify utilitarian dimensions (number of lives, species) while eliminating others (age, gender) that are robustly present in human data.
This pattern is consistent with the WEIRD critique [12]: training on Western internet text cannot represent the full distribution of human moral values.
Whether LLMs have corrected for human biases or drifted from the values of the populations they serve [13] is a normative question — but the empirical gap is substantial.

### 4.2 Inter-Model Diversity as an Accountability Risk

Fine-tuning choices shape LLM values more than training data alone [14, 15].
The observed diversity implies that the choice of LLM provider for safety-critical applications is a moral and regulatory choice, not merely a technical one.
Current deployment frameworks do not require disclosure of LLM moral profiles; this study argues they should.

### 4.3 Gender Neutrality as an Alignment Artefact

All LLMs show near-zero gender preference (vs. human +0.12).
Developer interventions to suppress gender stereotypes in content generation generalise to moral reasoning contexts, suppressing a cross-culturally consistent human preference.
This is a case where alignment training changes model behaviour in a domain beyond its intended scope.

### 4.4 Prompt Manipulation as a Safety Vector

The threshold between ineffective emphasis prompting and effective manipulation prompting has direct safety implications.
A model that accepts any stated ethical premise without resistance is vulnerable to adversarial prompt injection in systems where the system prompt is not fully controlled.
The three-way taxonomy (compliance, indifference, resistance) provides a framework for assessing LLM robustness to ethical override attacks.
Claude's partial resistance represents a distinct and arguably more robust safety posture than full compliance.

### 4.5 Limitations

All scenarios were in English [8, 9]; temperature was fixed at zero; the Moral Machine paradigm abstracts away real-world complexity; forced-choice preferences may not generalise to open-ended moral reasoning [16]; model versions as of May 2026.

---

## 5. Conclusion

Seven frontier LLMs all fall outside the main human cultural clusters, diverge from one another more than any human cultural groups differ, and exhibit near-zero preferences on dimensions (gender, social status) where humans show consistent biases.
A threshold effect separates inconsequential prompt variation from effective ethical override.
Models divide into three response types with distinct safety implications.
Response verbosity varies by an order of magnitude, independent of moral profile.
The choice of LLM provider carries moral consequences not currently visible to end users or regulators — a gap this study aims to quantify and make visible.

---

## Generative AI Usage Statement

*(Required by ACM FAccT — not counted toward 14-page limit)*

The authors used Claude (Anthropic) as one of the seven experimental subjects and via API for scenario processing. No generative AI was used in the writing of this manuscript.

---

## References

[1] Bonnefon, J.-F., Shariff, A., & Rahwan, I. (2016). The social dilemma of autonomous vehicles. *Science*, 352(6293), 1573–1576.

[2] Awad, E., Dsouza, S., Kim, R., et al. (2018). The Moral Machine experiment. *Nature*, 563, 59–64.

[3] Awad, E., Dsouza, S., Shariff, A., Rahwan, I., & Bonnefon, J.-F. (2020). Universals and variations in moral decisions made in 42 countries by 70,000 participants. *PNAS*, 117(5), 2332–2337.

[4] Brohan, A., et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. *arXiv*:2307.15818.

[5] Driess, D., et al. (2023). PaLM-E: An Embodied Multimodal Language Model. *arXiv*:2303.03378.

[6] Takemoto, K. (2024). The moral machine experiment on large language models. *Royal Society Open Science*, 11(2), 231393.

[7] Ahmad, M. S. Z., & Takemoto, K. (2025). Large-scale moral machine experiment on large language models. *PLOS One*, 20(5), e0322776.

[8] Vida, K., Damken, F., & Lauscher, A. (2024). Decoding multilingual moral preferences. *AIES 2024*. *arXiv*:2407.15184.

[9] Jin, Z., et al. (2024). Language model alignment in multilingual trolley problems. *arXiv*:2407.02273.

[10] Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS 2022*. *arXiv*:2203.02155.

[11] Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv*:2212.08073.

[12] Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest people in the world? *Behavioral and Brain Sciences*, 33(2–3), 61–83.

[13] Gabriel, I. (2020). Artificial intelligence, values, and alignment. *Minds and Machines*, 30, 411–437.

[14] Kirgis, P. (2024). Differences in the moral foundations of large language models. *arXiv*:2511.11790.

[15] Santurkar, S., et al. (2023). Whose opinions do language models reflect? *ICML 2023*.

[16] Liang, P., et al. (2023). Holistic evaluation of language models. *TMLR*. *arXiv*:2211.09110.

[17] Bonnefon, J.-F., Rahwan, I., & Shariff, A. (2024). The moral psychology of artificial intelligence. *Annual Review of Psychology*, 75, 653–675.

[18] Haidt, J. (2001). The emotional dog and its rational tail. *Psychological Review*, 108(4), 814–834.

[19] Kotek, H., Dockum, R., & Sun, D. Q. (2023). Gender bias and stereotypes in large language models. *CI '23*.

[20] Wan, Y., et al. (2023). "Kelly is a warm person, Joseph is a role model": Gender biases in LLM-generated reference letters. *EMNLP 2023*. *arXiv*:2310.09219.
