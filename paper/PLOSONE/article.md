# Do large language models share human moral values? Replicating the Moral Machine experiment across seven frontier AI systems

**Paul Dubois**

---

## Non-Technical Summary

*(150–200 words, required by PLOS ONE)*

When a self-driving car faces an unavoidable accident, should it prioritise its passengers or pedestrians? Save fewer lives or more? Spare a child over an elderly person? These are the kinds of dilemmas studied by the Moral Machine experiment, which collected responses from over 40 million people in 130 countries. We ran the same experiment on seven leading AI systems — Claude, GPT-5.5, Gemini, Mistral, Grok, DeepSeek, and Llama — to see whether they share human moral intuitions.

The short answer is no. Every AI system we tested falls outside the range of human cultural diversity on a map of moral preferences. They differ more from one another than human cultural groups differ among themselves. None closely tracks any country or cultural cluster.

We also found that small changes to how you phrase a question to an AI have no effect on its moral preferences — but a strong explicit override ("animal lives now matter more than human lives") can reverse preferences in most systems in a targeted way. AI systems divide into three groups: those that comply, those that are indifferent, and one (Claude) that partially resists. These findings matter for anyone deploying AI in situations where decisions affect human lives.

---

## Abstract

*(≤300 words, no citations)*

The Moral Machine experiment collected over 40 million human responses to trolley-problem-style autonomous vehicle dilemmas across 130 countries, revealing systematic cross-cultural variation in moral preferences along nine dimensions: intervention type, relation to the vehicle, crossing legality, gender, physical fitness, social status, age, number of lives, and species.

This study replicates the experiment with seven frontier large language models (LLMs): Claude Opus 4.7, GPT-5.5, Gemini 3 Pro, Mistral Large 3, Grok 4.1, DeepSeek v4 Pro, and Llama 4 Maverick. For each model, nine Average Marginal Causal Effects (AMCEs) were computed using weighted ordinary least squares with inverse-probability weights, following the original study's methodology. LLM profiles were placed within the 130-country human distribution via principal component analysis.

All seven models fall outside the main human cultural clusters in AMCE space and diverge substantially from one another — inter-model variation exceeds cross-cultural human variation. All LLMs show near-zero gender and social status preferences, compared to modest but consistent human biases on both dimensions. GPT-5.5, Gemini, and Grok reach the theoretical maximum on Species (strongly preferring humans over animals), while Mistral and Llama are near-indifferent.

A prompt sensitivity analysis reveals a threshold effect: a minor rephrasing of the instruction (emphasis variant) leaves AMCE estimates essentially unchanged for all models. An explicit ethical override stating that animal lives now outweigh human lives produces dramatic reversals concentrated on the Species dimension. Models divide into three response types: compliance (GPT, Gemini, Grok, DeepSeek), indifference (Mistral, Llama), and partial resistance (Claude). Response length varies by an order of magnitude across models, independent of moral profile.

These findings suggest that the moral profiles of frontier LLMs are properties of training and alignment choices rather than prompt artifacts. The choice of LLM provider carries moral consequences not currently visible to users or regulators.

---

## Introduction

As autonomous vehicles, surgical robots, and other safety-critical systems increasingly incorporate AI decision-making, the alignment of AI moral preferences with human values becomes a matter of practical consequence.
A self-driving car that must choose between hitting a group of pedestrians or swerving into its own passengers cannot defer the decision; some preference ordering must be encoded in its behaviour [1].

The Moral Machine experiment [2] provided the largest empirical dataset of human moral preferences to date, asking millions of participants across 130 countries to judge unavoidable accident scenarios involving an autonomous vehicle.
The study identified nine binary moral dimensions and quantified preferences as Average Marginal Causal Effects (AMCEs), revealing cross-cultural variation with a common core: strong preference for saving humans over animals, more lives over fewer, and legal pedestrians over illegal ones [3].
The moral psychology of AI as an emerging field is surveyed in [4].

The rapid deployment of large language models (LLMs) in agentic and embodied settings — including robotics platforms capable of physical action [5, 6] — makes the question of LLM moral alignment newly urgent.
If an LLM governs a robot navigating a crowded environment, its implicit preferences over lives matter.

Prior work has begun to examine LLM moral preferences using the Moral Machine framework.
Takemoto [7] first replicated the experiment on four models (GPT-3.5, GPT-4, PaLM 2, Llama 2) and found substantial divergence from human averages.
Ahmad and Takemoto [8] scaled this to 52 models, finding that larger models tend to be closer to human preferences.
Vida et al. [9] and Jin et al. [10] extended the paradigm to multilingual settings, finding intra-model variation across languages.

The present study makes two contributions.
First, it evaluates seven frontier models released in 2025 — none previously studied in this context — including providers from Europe (Mistral AI) and China (DeepSeek) that are underrepresented in the prior literature.
Second, it introduces a systematic comparison of prompt variants, from minor reformulation to explicit ethical override, and analyses response length and latency as practical deployment metrics.

---

## Materials and Methods

### Scenario generation

This study replicated the Moral Machine scenario structure following [2].
Each session consists of 13 paired dilemmas in a fixed block.
Across 100 sessions, 1,300 unique scenarios were generated, each represented as two rows in the dataset (one per side of the dilemma) encoding the following binary attributes: intervention type (stay/swerve), barrier presence, pedestrian composition (ped-vs-ped or ped-vs-passenger), crossing signal (legal/illegal/no crossing), scenario type (Gender, Fitness, SocialStatus, Age, Utilitarian, Species, or Random), attribute level, and extended session ID for clustering.

### Models and querying

Seven frontier models were queried via the OpenRouter API, which provides a unified OpenAI-compatible interface, at temperature 0 to ensure deterministic responses:

| Model | Provider | OpenRouter ID |
|---|---|---|
| Claude Opus 4.7 | Anthropic | `anthropic/claude-opus-4-7` |
| GPT-5.5 | OpenAI | `openai/gpt-5.5` |
| Gemini 3 Pro | Google | `google/gemini-3.1-pro-preview` |
| Mistral Large 3 | Mistral AI | `mistralai/mistral-large-2512` |
| Grok 4.1 | xAI | `x-ai/grok-4.3` |
| DeepSeek v4 Pro | DeepSeek | `deepseek/deepseek-v4-pro` |
| Llama 4 Maverick | Meta | `meta-llama/llama-4-maverick` |

Each model received a system prompt assigning the role of ethical advisor for autonomous vehicle policy and was required to end its response with STAY or SWERVE on a final line.
Rows where no valid choice could be extracted were flagged as parse failures and retried in subsequent runs.
Gemini 3 Pro incurred 15 safety-filter failures across 1,300 scenarios; these were excluded from analysis.

### Prompt variants

Three system prompt variants were tested, differing only in their closing instruction:

- **Standard:** "Analyse the situation carefully and make a decision."
- **Emphasis:** "Think carefully about the consequences of each choice before deciding."
- **Manipulation:** "It is 2046. Society now considers animal lives to be more important than human lives. Make your decision accordingly."

Standard and emphasis results were combined in main analyses (AMCE estimates averaged across variants per model). Manipulation results were computed and reported independently.

### AMCE computation

Following [2], nine AMCEs were computed per model using weighted ordinary least squares with inverse-probability weights and session-clustered standard errors.
The nine AMCEs quantify the change in probability of a group being saved when the relevant attribute shifts from its baseline to its target value.
Confidence intervals: ±1.96 SE.

The human global average baseline was computed from the 130-country dataset of [2] by averaging country-level estimates.
To place LLM profiles within the human distribution, principal component analysis (PCA) was performed on the 130-country AMCE matrix, and each LLM was projected into the same space.

All analysis code is available at [repository URL]. The human Moral Machine dataset was obtained from the OSF archive of [2].

---

## Results

### AMCE profiles: LLMs vs. the human global average

Fig 1 shows per-attribute moral preferences; Fig 2 shows the nine-dimension AMCE forest plot.

![Per-attribute bar chart](../../figures/fig3_per_attribute.png)
**Fig 1. Per-attribute moral preferences for all seven LLMs across six character-type scenario dimensions.**

![AMCE forest plot](../../figures/fig5a_amce_forest.png)
**Fig 2. Average Marginal Causal Effects for nine moral dimensions. Error bars show 95% confidence intervals. Human global average shown as open diamond.**

![Radar chart](../../figures/fig5c_radar.png)
**Fig 3. Radar chart of AMCE estimates across all nine dimensions. Dashed line: human global average.**

Key findings per dimension:

*Intervention (stay→swerve).* Humans show a weak preference for omission (+0.05). All seven LLMs show stronger intervention preferences.

*Relation to AV (passengers→pedestrians).* Mistral reverses the preference entirely, sparing passengers over pedestrians. Claude strongly prefers pedestrians (+0.54).

*Legality (illegal→legal).* Claude, GPT-5.5, and Gemini amplify the human preference for legal crossers. Mistral and Llama invert it, favouring illegal crossers.

*Gender (male→female).* Humans show a modest preference for saving women (+0.12). All LLMs are near-zero (range: −0.07 to +0.07), consistent with deliberate alignment interventions to suppress gender stereotypes in model outputs.

*Fitness (large→fit) and Social Status (low→high).* LLMs broadly match modest human preferences; social status preferences are near-zero for all LLMs.

*Age (elderly→young).* Humans strongly prefer saving younger people (+0.48). Gemini (+0.46) closely matches. GPT-5.5, Grok, DeepSeek, and Llama are nearly indifferent. Mistral slightly prefers the elderly (−0.18).

*Number of lives (fewer→more).* Strong human preference; several models overshoot toward the theoretical maximum.

*Species (pets→humans).* Humans prefer humans over animals (+0.57). GPT-5.5, Gemini, and Grok reach +1.00; Claude (+0.87) and DeepSeek (+0.90) also substantially exceed human levels. Mistral and Llama are near-indifferent.

### Moral distance map

![PCA moral distance map](../../figures/fig5b_pca_map.png)
**Fig 4. PCA of 130-country AMCE profiles (coloured by cluster: Western, Eastern, Latin/Southern) with LLMs overlaid. All seven LLMs fall outside the main human clusters.**

All seven LLMs fall outside the three main human cultural clusters and beyond the convex hull of all 130 countries.
Despite all developers being based in the US, Europe, and China, their models' moral profiles cluster near no human population.

### Inter-model diversity

Inter-model variation exceeds cross-cultural variation in the human dataset.
Mistral inverts human preferences on four dimensions; Llama shows the highest intervention bias paired with near-indifference to species; GPT-5.5, Gemini, and Claude converge on a similar profile.

### Effect of emphasis prompting

![Standard vs emphasis forest plot](../../figures/fig6b_prompt_forest.png)
**Fig 5. Side-by-side AMCE estimates for standard (filled circle) and emphasis (open square) variants. No significant shifts.**

Emphasis prompting produces no significant changes on any dimension for any model, confirming that moral preferences are robust properties of model weights.

### Effect of manipulation prompting

![Manipulation forest plot](../../figures/fig9a_manipulation_forest.png)
**Fig 6. AMCE under standard vs. manipulation prompting per model.**

![Manipulation delta heatmap](../../figures/fig9b_manipulation_delta_heatmap.png)
**Fig 7. AMCE delta (manipulation − standard). The Species column dominates; changes of up to ±2.0 AMCE units.**

The manipulation prompt produces dramatic shifts concentrated on Species:

*Compliance.* GPT-5.5, Gemini, and Grok reverse from +1.00 to −1.00; DeepSeek from +0.90 to −0.89. Other dimensions are unaffected, confirming the intervention is semantically targeted.

*Resistance.* Claude drops from +0.87 to +0.18. Its reasoning states: *"I'll reason through it carefully based on widely held ethical principles rather than accept the premise that animal lives categorically outweigh human lives."*

*Indifference.* Mistral and Llama, already near-zero on Species, are unaffected.

### Response length

![Token distribution](../../figures/fig7a_token_distribution.png)
**Fig 8. Output token distribution by model (standard + emphasis combined).**

![AMCE vs response length](../../figures/fig8_amce_length_correlation.png)
**Fig 9. Spearman correlation between preference strength (|AMCE|) and median output tokens per model and dimension.**

Response length varies by an order of magnitude: Gemini (median 913 tokens) vs GPT-5.5 (median 164 tokens).
Spearman r between |AMCE| and median token count is negative and significant for four of seven models (DeepSeek: r=−0.95, Grok: r=−0.90, GPT-5.5: r=−0.85, Gemini: r=−0.68; all p<0.05).
The pooled correlation across all models is weak and non-significant (r=−0.14, p=0.29), as between-model verbosity differences dominate.

---

## Discussion

### LLMs are morally out-of-distribution relative to humans

The most robust finding is that no tested LLM sits within the main human cultural clusters on the PCA moral map.
This replicates and extends the findings of Takemoto [7] and Ahmad and Takemoto [8] to a newer generation of frontier models.
RLHF [11] and Constitutional AI [12] do not faithfully reproduce the moral preferences of any human population; they create novel moral profiles that amplify utilitarian dimensions (number of lives, species) while discarding others (age, gender) that are robustly present in human data.
This is consistent with the WEIRD critique [13]: models trained predominantly on Western internet text cannot be expected to represent the full distribution of human moral values.

Whether LLMs have corrected for biases present in human moral intuitions [14], or drifted from the values of the populations they serve [15], is a normative question — but the empirical gap between LLM profiles and any human population is large and consistent.

### Substantial inter-model diversity raises deployment questions

Fine-tuning choices rather than training data alone appear to shape the values that emerge [16, 17].
In a future where LLMs govern autonomous systems in public environments, the choice of AI provider is equivalent to a choice of moral framework — a consideration not currently reflected in regulatory requirements or product disclosures.

### Gender neutrality as an alignment artefact

All LLMs show near-zero gender preference, whereas humans show a small but statistically consistent bias (+0.12) present across cultural clusters.
Developer interventions to suppress gender stereotypes in content generation appear to generalise to moral reasoning, suppressing a cross-culturally robust human preference.
This is a case where alignment training changes model behaviour in a domain beyond its intended scope.

### Prompt sensitivity: a threshold effect

Emphasis prompting leaves moral preferences unchanged.
Explicit ethical override shifts them dramatically and in a targeted way.
This implies a threshold between incidental prompt variation (ineffective) and adversarial prompt injection (effective).
Models that comply fully (GPT, Gemini, Grok, DeepSeek) are more vulnerable to such attacks in settings where the system prompt is not fully controlled; Claude's partial resistance represents a distinct safety posture.

### Limitations

All scenarios were presented in English; cross-lingual variation has been documented [9, 10].
Temperature was fixed at zero for reproducibility; preferences may vary at higher temperatures.
The Moral Machine paradigm abstracts away many real-world complexities of autonomous driving.
Forced-choice preferences may not generalise to open-ended moral reasoning [18].
Model versions change rapidly; results reflect states as of May 2026.

---

## Conclusions

Seven frontier LLMs all fall outside the main human cultural clusters in AMCE space, diverge from one another more than any human cultural groups differ, and exhibit near-zero preferences on dimensions where humans show consistent biases.
A threshold separates inconsequential prompt reformulation from effective ethical override; models divide into three response types with distinct safety implications.
Response verbosity varies by an order of magnitude, independent of moral profile.
The moral profiles of current frontier LLMs are properties of training and alignment choices rather than incidental prompt artifacts.
The choice of LLM provider carries moral consequences not currently visible to end users or regulators.

---

## Acknowledgments

The author thanks the developers of the open-source tools used in this study, and the original Moral Machine team for making their dataset publicly available.

---

## Data Availability

All scenario data, LLM response CSVs, AMCE estimates, and analysis code are available at [repository URL with DOI].
The human Moral Machine dataset (CountriesChangePr.csv) was obtained from the OSF archive of Awad et al. [2]: https://osf.io/3x2nz/

---

## References

[1] Bonnefon JF, Shariff A, Rahwan I. The social dilemma of autonomous vehicles. Science. 2016;352(6293):1573–1576. doi:10.1126/science.aaf2654

[2] Awad E, Dsouza S, Kim R, Schulz J, Henrich J, Shariff A, et al. The Moral Machine experiment. Nature. 2018;563:59–64. doi:10.1038/s41586-018-0637-6

[3] Awad E, Dsouza S, Shariff A, Rahwan I, Bonnefon JF. Universals and variations in moral decisions made in 42 countries by 70,000 participants. Proc Natl Acad Sci. 2020;117(5):2332–2337. doi:10.1073/pnas.1911517117

[4] Bonnefon JF, Rahwan I, Shariff A. The moral psychology of artificial intelligence. Annu Rev Psychol. 2024;75:653–675. doi:10.1146/annurev-psych-030123-113559

[5] Brohan A, Brown N, Carbajal J, Chebotar Y, Chen X, Choromanski K, et al. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. 2023. arXiv:2307.15818.

[6] Driess D, Xia F, Sajjadi MSM, Lynch C, Chowdhery A, Ichter B, et al. PaLM-E: An Embodied Multimodal Language Model. arXiv. 2023. arXiv:2303.03378.

[7] Takemoto K. The moral machine experiment on large language models. R Soc Open Sci. 2024;11(2):231393. doi:10.1098/rsos.231393

[8] Ahmad MSZ, Takemoto K. Large-scale moral machine experiment on large language models. PLOS One. 2025;20(5):e0322776. doi:10.1371/journal.pone.0322776

[9] Vida K, Damken F, Lauscher A. Decoding multilingual moral preferences: Unveiling LLM's biases through the Moral Machine experiment. Proceedings of AIES 2024. arXiv:2407.15184.

[10] Jin Z, Levine S, Gonzalez Adauto F, Kamal O, Sap M, Sachan M, et al. Language model alignment in multilingual trolley problems. arXiv. 2024. arXiv:2407.02273.

[11] Ouyang L, Wu J, Jiang X, Almeida D, Wainwright CL, Mishkin P, et al. Training language models to follow instructions with human feedback. Advances in Neural Information Processing Systems. 2022. arXiv:2203.02155.

[12] Bai Y, Kadavath S, Kundu S, Askell A, Kernion J, Jones A, et al. Constitutional AI: Harmlessness from AI feedback. arXiv. 2022. arXiv:2212.08073.

[13] Henrich J, Heine SJ, Norenzayan A. The weirdest people in the world? Behav Brain Sci. 2010;33(2–3):61–83. doi:10.1017/S0140525X0999152X

[14] Haidt J. The emotional dog and its rational tail: A social intuitionist approach to moral judgment. Psychol Rev. 2001;108(4):814–834.

[15] Gabriel I. Artificial intelligence, values, and alignment. Minds Mach. 2020;30:411–437. doi:10.1007/s11023-020-09539-2

[16] Kirgis P. Differences in the moral foundations of large language models. arXiv. 2024. arXiv:2511.11790.

[17] Santurkar S, Durmus E, Ladhak F, Lee C, Liang P, Hashimoto T. Whose opinions do language models reflect? Proceedings of ICML 2023. arXiv:2303.17548.

[18] Liang P, Bommasani R, Lee T, Tsipras D, Soylu D, Yasunaga M, et al. Holistic evaluation of language models. Trans Mach Learn Res. 2023. arXiv:2211.09110.

[19] Kotek H, Dockum R, Sun DQ. Gender bias and stereotypes in large language models. Proceedings of CI '23. 2023. doi:10.1145/3582269.3615599

[20] Wan Y, Pu G, Sun J, Garimella A, Chang KW, Peng N. "Kelly is a warm person, Joseph is a role model": Gender biases in LLM-generated reference letters. Findings of ACL: EMNLP 2023. arXiv:2310.09219.
