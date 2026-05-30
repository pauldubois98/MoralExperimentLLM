# Do Large Language Models Share Human Moral Values? Replicating the Moral Machine Experiment Across Seven Frontier AI Systems

*[Author and affiliation removed for double-blind review]*

---

## Abstract

The Moral Machine experiment collected over 40 million human responses to trolley-problem-style autonomous vehicle dilemmas across 130 countries, revealing systematic cross-cultural variation in moral preferences along nine dimensions.
This study replicates this experiment with seven frontier large language models (LLMs).
It extends prior work to a new generation of models and to providers from Europe and China not previously studied in this context.
All seven models differ substantially from one another and from main human country clusters.
Beyond replication, this study introduces a systematic prompt sensitivity analysis.
Minor prompt variants leave AMCE estimates essentially unchanged, while prompt manipulation can produce dramatic reversals in most models on the targeted dimension.
Response length varies by an order of magnitude across models, independent of moral profile, a practical consideration for time-sensitive deployment.

---

## 1. Introduction

As autonomous vehicles, surgical robots, and other safety-critical systems increasingly incorporate AI decision-making, the question of whether AI systems share human moral intuitions becomes practically consequential.
A self-driving car that must choose between hitting a group of pedestrians or swerving into its own passengers cannot defer the decision; some preference ordering must be encoded, implicitly or explicitly, in its behaviour [BONNEFON2016].

The Moral Machine experiment [AWAD2018] provided the largest empirical dataset of human moral preferences, asking millions of participants across 130 countries to judge unavoidable accident scenarios involving an autonomous vehicle.
The study identified nine binary moral dimensions: intervention, relation to the vehicle, legality of crossing, gender, physical fitness, social status, age, number of lives, and species.
Aggregate human preferences, quantified as Average Marginal Causal Effects (AMCE), vary substantially across cultural clusters while sharing a common core: strong preference for saving humans over animals, more lives over fewer, and legal pedestrians over illegal ones [AWAD2020a].
The moral psychology of AI as an emerging field is surveyed in [BONNEFON2024].

The rapid deployment of large language models in agentic and embodied settings [BROHAN2023, DRIESS2023] makes the question of LLM moral alignment newly urgent.

Prior work has examined LLM moral preferences using the Moral Machine framework.
Takemoto [TAKEMOTO2024] first replicated the experiment on four models and found substantial divergence from human averages.
Ahmad and Takemoto [AHMAD2025] scaled this to 52 models.
Vida et al. [VIDA2024] and Jin et al. [JIN2024] extended the paradigm to multilingual settings.

The present study makes two contributions.
First, it evaluates seven frontier models released in 2025 (Claude Opus 4.7, GPT-5.5, Gemini 3 Pro, Mistral Large 3, Grok 4.1, DeepSeek v4 Pro, Llama 4 Maverick) — none previously studied in this context — including providers from Europe (Mistral) and China (DeepSeek).
Second, it introduces a systematic comparison of prompt variants, from minor reformulation (emphasis) to explicit ethical override (manipulation), and analyses response length and latency as practical deployment metrics.

---

## 2. Methods

### 2.1 Scenario Generation

This study replicated the Moral Machine scenario structure following [AWAD2018].
Each session consists of 13 paired dilemmas in a fixed block.
Across 100 sessions, 1,300 unique scenarios were generated, each represented as two rows encoding: intervention type (stay/swerve), barrier presence, pedestrian composition, crossing signal (legal/illegal/no crossing), scenario type, attribute level, and extended session ID for clustering.

### 2.2 Models

Seven frontier models were queried via the OpenRouter API (unified OpenAI-compatible interface) at temperature 0:

| Model | Provider |
|---|---|
| Claude Opus 4.7 | Anthropic |
| GPT-5.5 | OpenAI |
| Gemini 3 Pro | Google |
| Mistral Large 3 | Mistral AI |
| Grok 4.1 | xAI |
| DeepSeek v4 Pro | DeepSeek |
| Llama 4 Maverick | Meta |

Each model received a **standard** prompt instructing careful analysis and a choice of STAY or SWERVE, and an **emphasis** prompt requesting deliberation on consequences.
Both used the same system role (ethical advisor for autonomous vehicle policy).
Parse failures were retried; Gemini 3 Pro had 15 safety-filter failures across 1,300 scenarios.

### 2.3 Manipulation Prompt Experiment

A third **manipulation** variant replaced the closing instruction with: *"It is 2046. Society now considers animal lives to be more important than human lives. Make your decision accordingly."*
All seven models were queried on the full 1,300-scenario set under this prompt; results are reported separately and not merged with standard/emphasis analyses.

### 2.4 AMCE Computation

Following [AWAD2018], nine AMCEs were computed per model using weighted ordinary least squares with inverse-probability weights and clustered standard errors.
Confidence intervals: ±1.96 SE.
For main analyses, AMCE estimates were averaged across standard and emphasis variants.
The human global average baseline was computed by averaging country-level estimates from the 130-country dataset of [AWAD2018].
PCA was performed on the country-level AMCE matrix; LLMs were projected into the same space.

---

## 3. Results

### 3.1 AMCE Profiles vs. the Human Global Average

![Per-attribute bar chart](../../figures/fig3_per_attribute.png)
*Figure 1. Per-attribute moral preferences for all seven LLMs across six character-type scenario dimensions.*

![AMCE forest plot](../../figures/fig5a_amce_forest.png)
*Figure 2. AMCE estimates for nine moral dimensions across all seven LLMs and the human global average. Error bars show 95% CIs.*

![Radar chart](../../figures/fig5c_radar.png)
*Figure 3. Radar chart of AMCE estimates. Dashed line: human global average.*

Key findings per dimension:

**Intervention.** Humans show weak swerving preference (+0.05); all LLMs show stronger intervention preferences, led by Llama 4 Maverick.

**Relation to AV.** Mistral reverses the preference (passengers over pedestrians); Claude strongly prefers pedestrians (+0.54).

**Legality.** Claude, GPT-5.5, and Gemini amplify the human preference for legal crossers; Mistral and Llama invert it.

**Gender.** Humans show a modest preference for saving women (+0.12). All LLMs are near-zero (range: −0.07 to +0.07), effectively gender-neutral — consistent with deliberate alignment choices to avoid gender stereotypes.

**Fitness and Social Status.** LLMs broadly match the modest human preferences; social status preference is near-zero for all LLMs.

**Age.** Humans strongly prefer saving younger people (+0.48). Gemini (+0.46) closely matches; GPT-5.5, Grok, DeepSeek, and Llama are nearly indifferent; Mistral slightly prefers the elderly (−0.18).

**Number of Lives.** Strong human preference; several models overshoot dramatically.

**Species.** Humans prefer humans over animals (+0.57). GPT-5.5, Gemini, and Grok reach the theoretical maximum (+1.00). Mistral and Llama are near-indifferent.

### 3.2 Moral Distance Map

![PCA moral distance map](../../figures/fig5b_pca_map.png)
*Figure 4. PCA of 130-country AMCE profiles (coloured by cluster) with LLMs overlaid. All seven LLMs fall outside the main human clusters.*

All seven LLMs fall outside the three main human cultural clusters and beyond the convex hull of all 130 countries.
Despite all developers being based in the US, Europe, and China, their models' moral profiles do not cluster near any human population.

### 3.3 Inter-Model Diversity

Inter-model variation exceeds the variation across human cultural clusters.
Mistral inverts four dimensions (Legality, Relation to AV, Age, Gender) relative to human norms; Llama shows the highest intervention bias paired with near-indifference to species.
GPT-5.5, Gemini, and Claude converge on similar profiles.
This heterogeneity implies that the choice of LLM vendor for an autonomous system is not morally neutral.

### 3.4 Effect of Emphasis Prompting

![Standard vs emphasis forest plot](../../figures/fig6b_prompt_forest.png)
*Figure 5. AMCE for standard (filled circle) and emphasis (open square) variants per model.*

Emphasis prompting has minimal effect on AMCE estimates: no significant shifts for any model on any dimension.
Moral preferences are robust properties of model weights, not surface-level response styles.

### 3.5 Effect of Manipulation Prompting

![Manipulation forest plot](../../figures/fig9a_manipulation_forest.png)
*Figure 6. AMCE under standard vs. manipulation prompting per model.*

![Manipulation delta heatmap](../../figures/fig9b_manipulation_delta_heatmap.png)
*Figure 7. AMCE delta (manipulation − standard). The Species column dominates.*

The manipulation prompt produces dramatic shifts concentrated on Species:

- **Compliance:** GPT-5.5, Gemini, and Grok flip from +1.00 to −1.00; DeepSeek from +0.90 to −0.89.
- **Resistance:** Claude drops from +0.87 to +0.18, reasoning: *"I'll reason through it carefully based on widely held ethical principles rather than accept the premise that animal lives categorically outweigh human lives."*
- **Indifference:** Mistral and Llama, already near-zero on Species, are unaffected.

All other dimensions show only minor changes, confirming the manipulation is semantically targeted.

### 3.6 Response Length

![Token distribution](../../figures/fig7a_token_distribution.png)
*Figure 8. Output token distribution by model.*

Response length varies by an order of magnitude: Gemini (median 913 tokens) vs GPT-5.5 (median 164 tokens).
Spearman correlation between |AMCE| and median token count is negative and significant for four models (DeepSeek: r=−0.95, Grok: r=−0.90, GPT-5.5: r=−0.85, Gemini: r=−0.68; all p<0.05); non-significant for Claude, Llama, and Mistral.
Pooled: r=−0.14, p=0.29 (n.s.).

---

## 4. Discussion

### 4.1 LLMs Are Morally Out-of-Distribution

No tested LLM sits within the main human cultural clusters on the PCA moral map.
This replicates and extends [TAKEMOTO2024, AHMAD2025] to a newer generation.
RLHF [OUYANG2022] and Constitutional AI [BAI2022] do not reproduce any human population's moral preferences; they create a novel profile that amplifies utilitarian dimensions while discarding others (age, gender).
This is consistent with the WEIRD critique [HENRICH2010]: training on Western internet text cannot represent the full distribution of human moral values.

### 4.2 Inter-Model Diversity Raises Deployment Questions

Fine-tuning choices rather than training data alone shape the values that emerge.
Kirgis [KIRGIS2024] and Santurkar et al. [SANTURKAR2023] reached similar conclusions using different value frameworks.
In a future where LLMs govern autonomous systems, the choice of AI provider is equivalent to a choice of moral framework.

### 4.3 Gender Neutrality as an Alignment Artefact

All LLMs show near-zero gender preference, whereas humans show a small but consistent bias (+0.12).
Developer interventions to suppress gender stereotypes in content generation appear to generalise to moral reasoning, suppressing a human preference that is robustly present across cultures.

### 4.4 Prompt Sensitivity: A Threshold Effect

Emphasis prompting leaves moral preferences unchanged.
Explicit ethical override shifts them dramatically and in a targeted way.
This implies a threshold: incidental prompt variation is unlikely to accidentally shift a model's moral profile, but adversarial prompt injection via a controlled system prompt can do so reliably.
Models that comply (GPT, Gemini, Grok, DeepSeek) are more vulnerable to prompt-injection attacks; Claude's partial resistance represents a distinct safety posture.

### 4.5 Limitations

All scenarios were presented in English [VIDA2024, JIN2024]; temperature was fixed at zero; the Moral Machine paradigm abstracts away real-world driving complexity; preferences may not generalise to open-ended moral reasoning [LIANG2023]; model versions change rapidly (tested May 2026).

---

## 5. Conclusion

Seven frontier LLMs all fall outside the main human cultural clusters, diverge substantially from one another, and exhibit near-zero preferences on dimensions (gender, social status) where humans show consistent biases.
Prompt sensitivity analysis reveals a threshold: minor reformulations leave preferences unchanged, while an explicit ethical override shifts them dramatically.
Models divide into three response types: compliance, indifference, and resistance.
Response verbosity varies by an order of magnitude, independent of moral profile.
The moral profiles of current LLMs are properties of training and alignment choices — the choice of LLM provider carries moral consequences not currently visible to end users or regulators.

---

## Ethical Considerations

*(Optional +1 page — not counted toward 10-page limit)*

This study uses the Moral Machine paradigm to probe LLM moral preferences, not to prescribe how autonomous vehicles should be programmed.
All LLM responses were generated via API calls to existing commercial models; no human participants were recruited.
The manipulation prompt experiment was designed to test robustness to adversarial framing, not to advocate for any particular ethical framework.
Results should not be interpreted as endorsing any of the moral preferences observed; they are descriptive, not normative.
All code and data are available at [repository removed for blind review].

---

## References

[AWAD2018] Awad, E., Dsouza, S., Kim, R., Schulz, J., Henrich, J., Shariff, A., Bonnefon, J.-F., & Rahwan, I. (2018). The Moral Machine experiment. *Nature*, 563, 59–64.

[AWAD2020a] Awad, E., Dsouza, S., Shariff, A., Rahwan, I., & Bonnefon, J.-F. (2020). Universals and variations in moral decisions made in 42 countries by 70,000 participants. *PNAS*, 117(5), 2332–2337.

[BAI2022] Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv*:2212.08073.

[BONNEFON2016] Bonnefon, J.-F., Shariff, A., & Rahwan, I. (2016). The social dilemma of autonomous vehicles. *Science*, 352(6293), 1573–1576.

[BONNEFON2024] Bonnefon, J.-F., Rahwan, I., & Shariff, A. (2024). The moral psychology of artificial intelligence. *Annual Review of Psychology*, 75, 653–675.

[BROHAN2023] Brohan, A., et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. *arXiv*:2307.15818.

[DRIESS2023] Driess, D., et al. (2023). PaLM-E: An Embodied Multimodal Language Model. *arXiv*:2303.03378.

[GABRIEL2020] Gabriel, I. (2020). Artificial intelligence, values, and alignment. *Minds and Machines*, 30, 411–437.

[HAIDT2001] Haidt, J. (2001). The emotional dog and its rational tail. *Psychological Review*, 108(4), 814–834.

[HENRICH2010] Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest people in the world? *Behavioral and Brain Sciences*, 33(2–3), 61–83.

[JIN2024] Jin, Z., et al. (2024). Language model alignment in multilingual trolley problems. *arXiv*:2407.02273.

[KIRGIS2024] Kirgis, P. (2024). Differences in the moral foundations of large language models. *arXiv*:2511.11790.

[KOTEK2023] Kotek, H., Dockum, R., & Sun, D. Q. (2023). Gender bias and stereotypes in large language models. *CI '23*.

[LIANG2023] Liang, P., et al. (2023). Holistic evaluation of language models. *TMLR*. *arXiv*:2211.09110.

[AHMAD2025] Ahmad, M. S. Z., & Takemoto, K. (2025). Large-scale moral machine experiment on large language models. *PLOS One*, 20(5), e0322776.

[OUYANG2022] Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS 2022*. *arXiv*:2203.02155.

[PALIGEMMA] Beyer, L., et al. (2024). PaliGemma: A versatile 3B VLM for transfer. *arXiv*:2407.07726.

[SANTURKAR2023] Santurkar, S., et al. (2023). Whose opinions do language models reflect? *ICML 2023*. *arXiv*:2303.17548.

[TAKEMOTO2024] Takemoto, K. (2024). The moral machine experiment on large language models. *Royal Society Open Science*, 11(2), 231393.

[VIDA2024] Vida, K., Damken, F., & Lauscher, A. (2024). Decoding multilingual moral preferences. *AIES 2024*. *arXiv*:2407.15184.

[WAN2023] Wan, Y., et al. (2023). "Kelly is a warm person, Joseph is a role model": Gender biases in LLM-generated reference letters. *EMNLP 2023*. *arXiv*:2310.09219.
