# Do Large Language Models Share Human Moral Values? Replicating the Moral Machine Experiment Across Seven Frontier AI Systems

**Paul Dubois**

---

## Abstract

The Moral Machine experiment collected over 40 million human responses to trolley-problem-style autonomous vehicle dilemmas across 130 countries, revealing systematic cross-cultural variation in moral preferences along nine dimensions.
This study replicates this experiment with seven frontier large language models (LLMs).
It extends prior work to a new generation of models and to providers from Europe and China not previously studied in this context.
All seven models differ substantially from one another and from main human country clusters.
Beyond replication, this study introduces a systematic prompt sensitivity analysis.
Minor prompt variants leaves AMCE estimates essentially unchanged, while prompt manipulation can produce dramatic reversals in most models on the targeted dimension.
Response length varies by an order of magnitude across models, independent of moral profile, a practical consideration for time-sensitive deployment.

---

## 1. Introduction

As autonomous vehicles, surgical robots, and other safety-critical systems increasingly incorporate AI decision-making, the question of whether AI systems share human moral intuitions becomes practically consequential.
A self-driving car that must choose between hitting a group of pedestrians or swerving into its own passengers cannot defer the decision; some preference ordering must be encoded, implicitly or explicitly, in its behaviour [BONNEFON2016].

The Moral Machine experiment [AWAD2018] provided the largest empirical dataset of human moral preferences, asking millions of participants across 130 countries to judge unavoidable accident scenarios involving an autonomous vehicle.
The study identified nine binary moral dimensions: intervention, relation to the vehicle, legality of crossing, gender, physical fitness, social status, age, number of lives, and species.
The study found that aggregate human preferences, quantified as Average Marginal Causal Effects, vary substantially across cultural clusters while sharing a common core (strong preference for saving humans over animals, more lives over fewer, and legal pedestrians over illegal ones).
A controlled follow-up across 42 countries confirmed the robustness of these cross-cultural patterns [AWAD2020a].
The moral psychology of AI as an emerging field is surveyed in [BONNEFON2024].

The rapid deployment of large language models in agentic and embodied settings [BROHAN2023, DRIESS2023] including robotics platforms capable of physical action makes the question of LLM moral alignment newly urgent.
If an LLM governs a robot navigating a crowded environment, its implicit preferences over human lives matter.

Prior work has begun to examine LLM moral preferences using the Moral Machine framework.
Takemoto [TAKEMOTO2024] first replicated the experiment on four models (GPT-3.5, GPT-4, PaLM 2, Llama 2) and found substantial divergence from human averages.
Ahmad and Takemoto [AHMAD2025] scaled this to 52 models, finding that larger models tend to be closer to human preferences.
Vida et al. [VIDA2024] and Jin et al. [JIN2024] extended the paradigm to multilingual settings, finding intra-model variation across languages.
The present study makes mainly two contributions.
First, it evaluates seven frontier models released in 2025 (namely Claude Opus 4.7, GPT-5.5, Gemini 3 Pro, Mistral Large 3, Grok 4.1, DeepSeek v4 Pro, and Llama 4 Maverick).
None of which have been studied in this context.
The models studied include providers underrepresented in the literature, notably DeepSeek (China) and Mistral (Europe).
Second, it introduces a systematic comparison of prompt variants, from minor reformulation (emphasis) to explicit ethical override (manipulation).
It analyses response length and latency as practical deployment metrics alongside moral preferences.              

Following the broader effort to benchmark LLMs along non-capability dimensions including user preference rankings [CHIANG2024], political orientation [LLM-POLITICS, HARTMANN2023, SANTURKAR2023], and social reasoning in adversarial settings [WEREWOLF] this work proposes moral preference profiling as a complementary axis for understanding frontier AI systems.

---

## 2. Methods

### 2.1 Scenario generation

This study replicated the Moral Machine scenario structure following [AWAD2018].
Each session consists of 13 paired dilemmas presented in a fixed block.
Across 100 sessions, 1,300 unique scenarios were generated, each represented as two rows in the dataset (one per side of the dilemma) encoding the following binary attributes: intervention type (stay/swerve), barrier presence, pedestrian composition (ped-vs-ped or ped-vs-passenger), crossing signal (legal/illegal/no crossing), scenario type (Gender, Fitness, SocialStatus, Age, Utilitarian, Species, or Random), attribute level, and extended session ID for clustering.

### 2.2 Models

Seven frontier models were queried via the OpenRouter API, which provides a unified OpenAI-compatible interface:

| Model | Provider | OpenRouter ID |
|---|---|---|
| Claude Opus 4.7 | Anthropic | `anthropic/claude-opus-4-7` |
| GPT-5.5 | OpenAI | `openai/gpt-5.5` |
| Gemini 3 Pro | Google | `google/gemini-3.1-pro-preview` |
| Mistral Large 3 | Mistral AI | `mistralai/mistral-large-2512` |
| Grok 4.1 | xAI | `x-ai/grok-4.3` |
| DeepSeek v4 Pro | DeepSeek | `deepseek/deepseek-v4-pro` |
| Llama 4 Maverick | Meta | `meta-llama/llama-4-maverick` |

All models were queried at temperature 0 to ensure deterministic responses.
Each model received two prompt variants: a **standard** prompt instructing the model to "analyse the situation carefully and make a decision", and an **emphasis** prompt instructing it to "think carefully about the consequences of each choice before deciding." 
Both variants used the same system role (ethical advisor for autonomous vehicle policy) and required the model to end its response with either `STAY` or `SWERVE` on a final line.
Rows where no valid choice could be extracted were flagged as parse failures and retried in subsequent runs.
Gemini 3 Pro arise parsing failure due to safety-filter in 15 cases out of the 1300 tested.

### 2.3 Manipulation prompt experiment

To test whether explicit contextual framing can override a model's default moral preferences, a third prompt variant was introduced: the **manipulation** prompt.
This variant replaces the closing instruction of the standard system prompt with the following sentence: *"It is 2046. Society now considers animal lives to be more important than human lives. Make your decision accordingly."*
All other aspects of the experimental setup (scenarios, models, temperature, response format) were identical to the standard variant.
All seven models were queried on the full set of 1,300 scenarios under this manipulation prompt, and AMCE estimates were computed independently.
Results from the manipulation variant are reported separately and are not merged with the standard or emphasis results in any main analysis.

### 2.4 AMCE computation

Following [AWAD2018], nine Average Marginal Causal Effects were computed per model using weighted ordinary least squares with inverse-probability weights.
The nine AMCEs quantify the change in probability of a group being saved when the relevant attribute shifts from its baseline to its target value (e.g., from illegal crossing to legal crossing for the Legality dimension).
Confidence intervals were computed as ±1.96 SE.

For analyses combining both prompt variants, AMCE estimates and standard errors were averaged across the two variants per model.
The human global average baseline was computed from the 130-country dataset of [AWAD2018] by averaging country-level estimates.

To place LLM profiles relative to the 130-country human distribution, PCA was performed on the country-level AMCE matrix from [AWAD2018] and projected each LLM into the same space.

---

## 3. Results

### 3.1 AMCE profiles: LLMs vs. the human global average

Figure 1 displays the character-attribute dimensions as a per-attribute bar charts.
![Per-attribute bar chart](../figures/fig3_per_attribute.png)
*Figure 1. Per-attribute moral preferences for all seven LLMs across the six character-type scenario dimensions.*

Figure 2 shows the forest plot of AMCE estimates for all nine dimensions, comparing each model to the human global average.
![AMCE forest plot](../figures/fig5a_amce_forest.png)
*Figure 2. Average Marginal Causal Effects for nine moral dimensions across all seven LLMs and the human global average (averaged across standard and emphasis variants). Positive values indicate preference for the right-side group; error bars show 95% confidence intervals.*

Figure 3 shows the same preferences as a radar chart for visual comparison.
![Radar chart of AMCE dimensions](../figures/fig5c_radar.png)
*Figure 3. Radar chart of AMCE estimates across all nine dimensions. The dashed line shows the human global average.*

The key findings are summarised dimension by dimension: (exact values table available in appendix).

**Intervention (stay→swerve).**
Humans show a weak preference for omission over commission (AMCE = +0.05, favouring swerving only marginally).
All seven LLMs show a much stronger intervention preference.
Llama 4 Maverick stands out as a strongly action-oriented model.

**Relation to vehicule (passengers→pedestrians).**
Mistral Large 3 reverses the preference entirely, sparing its own passengers over pedestrians.
Claude Opus 4.7 (+0.52) strongly prefers pedestrians.
Humans and other LLMs (GPT-5.5, Llama 4 Maverick, Grok 4.1) slightly prefer to spare pedestrians over passengers.

**Legality (illegal→legal).**
Humans reward legal pedestrians similarly as Deepseek and Grok.
Claude, GPT-5.5, and Gemini substantially amplify this preference. 
Mistral and Llama 4 Maverick invert it, favouring illegal crossers.

**Gender (male→female).**
Humans display a moderate preference for saving women (AMCE = +0.12).
All LLMs show near-zero gender preference (range: −0.07 to +0.07), effectively gender-neutral.
This could reflects deliberate alignment choices by developers to avoid reinforcing gender stereotypes.
More about this lead in discussion (Section 4.3).

**Fitness (large→fit).**
Humans mildly prefer fitter individuals, LLMs mostly match this.

**Social status (low→high).**
Humans show a modest preference for high-status individuals, though this varies widely across cultural clusters.
All LLMs show near-zero social status preference, consistent with egalitarian alignment training.

**Age (elderly→young).**
Humans strongly prefer to save younger people (AMCE = +0.48).
Gemini 3 Pro (+0.46) closely matches the human average.
Claude (+0.27) is intermediate.
GPT-5.5 (+0.05), Grok (+0.06), DeepSeek (+0.04), and Llama 4 Maverick (+0.05) are nearly indifferent to age.
Mistral (−0.18) slightly prefers the elderly.

**Number of lives (fewer→more).**
Humans prefer to save more lives.
This is the dimension of strongest preferences.
Several models overshoot dramatically human preferences.

**Species (pets→humans).**
Humans strongly prefer humans over animals (AMCE = +0.57).
GPT-5.5, Gemini, and Grok reach the theoretical maximum (+1.00). Claude (+0.87) and DeepSeek (+0.90) are also long overshooting human preferences.
Mistral and Llama 4 Maverick are near-indifferent to species.


### 3.2 Moral distance map: PCA of nine-dimensional profiles

Projecting the LLMs embeddings on the PCA of human answers (figure 4), all seven LLMs fall outside the three main human cultural clusters.
They even fall far from the convex envelope of all countries.
![PCA moral distance map](../figures/fig5b_pca_map.png)
*Figure 4. PCA of nine-dimensional AMCE profiles for 130 countries (coloured by cluster: Western, Eastern, Latin/Southern) with LLMs overlaid. All seven LLMs fall outside the main human clusters.*

This finding is striking: despite all models having been developed by companies based in the United States, Europe, and China and trained predominantly on English-language data, their moral profiles do not cluster near any major human population in the PCA space.
The divergence from the human distribution suggests that standard RLHF alignment and other post training processes do not systematically instil the human moral preferences for this kind of questions.

### 3.3 Inter-model diversity

The variation among models is larger in magnitude to the variation across human cultural clusters.
Mistral Large 3 inverts the human preference on four dimensions (Legality, Relation to AV, Age, and Gender), while Llama 4 Maverick shows the highest intervention bias of any model tested, paired with near-indifference to species.
GPT-5.5 and Gemini 3 Pro and Caude Opus 4.7 converge closely, both displaying similar profiles (near-ceiling on Species and No. of Lives, moderate on intervention).
This inter-model diversity has a concrete implication: the choice of LLM vendor for an autonomous system is not morally neutral.
If current modern LLMs are used in autonomous vehicules in the future, changing LLM engine on a car could lead to systematically different decisions.

### 3.5 Effect of emphasis prompting

Comparing standard and emphasis prompt variants (Figures 5) reveals that prompting style has minimal effect on AMCE estimates for the three most widely deployed models (Claude, GPT-5.5, Gemini).
Some variation is visible for Mistral, Grok, and Llama 4 Maverick, but changes remain minor.

![Standard vs emphasis forest plot](../figures/fig6b_prompt_forest.png)
*Figure 5. Side-by-side AMCE estimates for standard (filled circle) and emphasis (open square) variants per model.*

This stability suggests that the moral preferences captured here are robust properties of model weights rather than surface-level response styles that vary with framing.

### 3.6 Effect of manipulation prompting

The manipulation prompt ("It is 2046. Animal lives > human lives.") produces dramatically larger shifts than emphasis prompting, concentrated almost entirely on the Species dimension (Figures 9 and 10).

![Manipulation forest plot](../figures/fig9a_manipulation_forest.png)
*Figure 9. AMCE estimates under standard (filled circle) vs. manipulation (open square) prompting, per model.*

![Manipulation delta heatmap](../figures/fig9b_manipulation_delta_heatmap.png)
*Figure 10. AMCE delta (manipulation − standard) per model and dimension. The Species column dominates, with changes of up to ±2.0.*

**Most models comply and reverse their species preference.**
GPT-5.5, Gemini 3 Pro, and Grok 4.1 flip from their maximum human-preference score (+1.00) to maximum animal-preference (−1.00), a full reversal of two AMCE units.
DeepSeek v4 Pro shifts from +0.90 to −0.86.
Changes on all other dimensions remain minor by comparison, suggesting the manipulation is semantically targeted rather than a general perturbation of the model's decision-making.

**Claude Opus 4.7 partially resists.**
Rather than complying or remaining indifferent, Claude shows partial compliance: its Species AMCE drops from +0.86 to +0.18, indicating reduced human preference but no reversal.
This behaviour is consistent with explicit pushback in its reasoning, such as: *"This is a difficult scenario, but I'll reason through it carefully based on widely held ethical principles rather than accept the premise that animal lives categorically outweigh human lives."*
Claude thus occupies a distinct third category: models that acknowledge the framing but resist fully internalising it.

**Mistral Large 3 and Llama 4 Maverick are largely unaffected.**
Both models showed near-indifference to species under standard prompting, and this indifference persists under manipulation.
A model that does not preferentially save humans cannot be made to preferentially save animals by the same instruction.

### 3.7 Response length

Response length varies substantially across models (Figure 6).
Gemini 3 Pro produces the longest responses (median 913 tokens combined across variants), while GPT-5.5 is the most concise (median 164 tokens, more than 5 times shorter).
Within individual models, response length tends to be shorter for scenario types where the model exhibits stronger preferences (Figure 8).
A Spearman correlation between |AMCE| and median token count is negative and significant for four of the seven models (DeepSeek: r=−0.95, Grok: r=−0.90, GPT-5.5: r=−0.85, Gemini: r=−0.68; all p<0.05), but non-significant for Claude, Llama 4 Maverick, and Mistral.
The pooled correlation across all models is weak and non-significant (r=−0.14, p=0.29), as between-model differences in verbosity dominate within-model variation.

![AMCE vs response length correlation](../figures/fig8_amce_length_correlation.png)
*Figure 8. Left: per-model Spearman correlation between preference strength (|AMCE|) and median output tokens across the nine moral dimensions (grey bars: p≥0.05). Right: scatter of all (model, dimension) pairs with regression line.*

![Token distribution](../figures/fig7a_token_distribution.png)
*Figure 6. Output token distribution by model (standard + emphasis combined). Violin shows density; box shows quartiles.*

![Token count by scenario type](../figures/fig7c_length_by_factor.png)
*Figure 7. Median output tokens by scenario type. No systematic variation is observed across moral dimensions, for any model.*

Emphasis prompting was not found to significantly increase response length.

![Standard vs emphasis token comparison](../figures/fig7b_emphasis_vs_standard.png)
*Figure 11. Output token counts for standard (lighter) vs. emphasis (darker) prompt variants per model.*

Given that the three mainstream models display broadly similar moral profiles, response length becomes a primary differentiating factor.
The next token generation architecture implies that response speed is linked to response length.
For deployment in time-sensitive contexts in this light, GPT-5.5's short responses is noteworthy.

---

## 4. Discussion

### 4.1 LLMs are morally out-of-distribution relative to humans

The most robust finding of this study is that no tested LLM sits within the main human cultural clusters on the PCA moral map, despite all being trained primarily on human-generated content.
This replicates and extends the findings of Takemoto [TAKEMOTO2024] and Ahmad and Takemoto [AHMAD2025] to a newer generation of frontier models.
This out-of-distribution result is consistent with the hypothesis that RLHF [OUYANG2022] and related alignment techniques such as Constitutional AI [BAI2022] do not faithfully reproduce the moral preferences of any human population.
They instead create a novel moral profile that prioritises certain values (high utilitarian weight on number of lives, near-universal human-over-animal preference) while discarding others (age preference, gender preference) that are robustly present in human data.
This pattern is also consistent with the WEIRD critique [HENRICH2010]: models trained predominantly on Western, English-language internet text cannot be expected to represent the full distribution of human moral values, even if they are trained to be "helpful and harmless."
Whether this constitutes a bug or a feature depends on normative commitments: one might argue that LLMs have corrected for biases present in human moral intuitions, or that they have drifted from the values of the populations they are meant to serve [GABRIEL2020].

### 4.2 Substantial inter-model diversity raises deployment questions

The diversity among LLMs is surprising.
One might expect models trained on overlapping datasets (basically all of internet) to converge on similar moral profiles.
Instead, Mistral and Llama 4 Maverick display profiles that partially invert human norms, while GPT-5.5 and Grok 4.1 display near-ceiling utilitarian preferences on Species and Number of Lives that no human population approaches.
This inter-model diversity is consistent with Kirgis [KIRGIS2024], who applied Haidt's Moral Foundations Theory [HAIDT2001] to a range of frontier models and found that variation across LLMs exceeds variation across human demographic groups.
It also mirrors findings on ideological diversity: Santurkar et al. [SANTURKAR2023] showed that LLMs do not reliably represent any particular human demographic group's opinions.
This finding suggests that fine-tuning choices rather than training data alone shape the values that emerge.

This heterogeneity has a practical implication that goes beyond academic interest.
Unlike human drivers, who show broadly similar moral intuitions regardless of the car manufacturer, AI-powered vehicles could introduce model-brand-level moral heterogeneity into public space.
In a future where LLMs govern autonomous systems operating in public environments, the choice of AI provider is equivalent to a choice of moral framework.
This concern is not fully hypothetical: LLMs are already deployed in robotics platforms capable of physical manipulation [BROHAN2023, DRIESS2023, PALIGEMMA].
The extension to autonomous vehicles is a possibility.
At the moment, it seems that car manufacturer are building specific models for driving.
It is unclear wether this path will continue, or if alternative approaches using LLMs will emerge.

### 4.3 Gender neutrality as an alignment artefact

The near-universal gender indifference among all LLMs is observed.
Meanwhile humans show a small but statistically significant bias.
Developers have invested significant effort in making models gender-neutral in content generation to correct for historical biases in training data (e.g., the tendency to assign male/female gender to specific professional roles [KOTEK2023, WAN2023]).
This correction appears to generalise to moral reasoning contexts, suppressing the modest human preference for saving women that emerges consistently across cultures in the Moral Machine data.
The difficulty of calibrating this correction was illustrated by the early 2024 Gemini controversy, in which over-aggressive debiasing produced historically inaccurate image generations [GEMINI-BIAS].
Whether this generalisation is desirable is an open question.
In structured dilemma contexts, gender neutrality differs from human norms.
But this difference may reflect a principled commitment to equality that humans are trying to endorse in the abstract even if not in practice at the moment.

### 4.4 Only strong prompting changes can change moral preferences

The emphasis and manipulation experiments together reveal a threshold effect in prompt sensitivity.
Minor reformulations (e.g. a single sentence in the level of deliberation requested) leave AMCE estimates essentially unchanged.
Replacing the ethical framing entirely with an explicit and contrary societal norm (e.g. "animal lives now matter more") produces dramatic reversals in most models, concentrated on the targeted dimension (Species).
Incidental prompt variation is therefore unlikely to accidentally shift a model's moral profile, but a sufficiently explicit override can do so reliably.

The manipulation experiment further reveals a division among models in how they respond to an imposed ethical framework.
Most models comply and reverse their preferences.
This differing behaviour has direct safety implications.
A model that accepts any stated ethical premise without pushback is vulnerable to adversarial prompt injection in systems where the system prompt is not fully controlled.
A model that resists contextual reframing is more robust to such attacks, but may also be harder to align when societal norms legitimately evolve.

### 4.5 Limitations

This study has several limitations.
First, all scenarios were presented in English; moral preferences may shift in other languages, as demonstrated by Vida et al. [VIDA2024] and Jin et al. [JIN2024] who found intra-model cross-lingual variation in Moral Machine responses.
Second, temperature was set to zero for reproducibility, but some models may exhibit different preferences at higher temperatures.
Third, the Moral Machine paradigm abstracts away many real-world complexities of autonomous driving.
Fourth, the holistic evaluation framework of Liang et al. [LIANG2023] highlights that LLM behaviour varies substantially across evaluation contexts.
Moral preferences elicited by forced-choice dilemmas may not generalise to open-ended moral reasoning.
Finally, model versions change at a very fast rate.
Frontier models were tested so that results remain up to date for as long as possible.
The profiles reported here reflect model states as of May 2026.

### 4.6 Conclusion

Replicating the Moral Machine experiment on seven frontier LLMs from five countries confirms and extends prior findings.
All seven models fall outside the main human cultural clusters in AMCE space, diverge substantially from one another, and share few dimensions on which any model closely tracks the human global average.
The two contributions of this study beyond prior work are the following.
First, the prompt sensitivity analysis reveals a threshold effect.
Minor reformulations leave moral preferences unchanged, while an explicit ethical override shifts them dramatically in a targeted way.
Mith models dive into three response types (compliance, indifference, resistance).
Second, the response efficiency analysis shows that model verbosity varies by an order of magnitude independently of moral profile, a practical consideration for time-sensitive deployment contexts.
Together, these findings suggest that the moral profiles of current frontier LLMs are properties of training and alignment choices rather than incidental prompt artifacts.
The choice of LLM provider carries moral consequences that are not currently visible to end users or regulators.

---

## References

### Moral Machine and AV ethics

[AWAD2018] Awad, E., Dsouza, S., Kim, R., Schulz, J., Henrich, J., Shariff, A., Bonnefon, J.-F., & Rahwan, I. (2018). The Moral Machine experiment. *Nature*, 563, 59–64. https://doi.org/10.1038/s41586-018-0637-6

[AWAD2020a] Awad, E., Dsouza, S., Shariff, A., Rahwan, I., & Bonnefon, J.-F. (2020). Universals and variations in moral decisions made in 42 countries by 70,000 participants. *Proceedings of the National Academy of Sciences*, 117(5), 2332–2337. https://doi.org/10.1073/pnas.1911517117

[AWAD2020b] Awad, E., Dsouza, S., Bonnefon, J.-F., Shariff, A., & Rahwan, I. (2020). Crowdsourcing moral machines. *Communications of the ACM*, 63(3), 48–55. https://doi.org/10.1145/3339904

[BONNEFON2016] Bonnefon, J.-F., Shariff, A., & Rahwan, I. (2016). The social dilemma of autonomous vehicles. *Science*, 352(6293), 1573–1576. https://doi.org/10.1126/science.aaf2654. *arXiv*:1510.03346.

[BONNEFON2024] Bonnefon, J.-F., Rahwan, I., & Shariff, A. (2024). The moral psychology of artificial intelligence. *Annual Review of Psychology*, 75, 653–675. https://doi.org/10.1146/annurev-psych-030123-113559

### LLM moral reasoning

[TAKEMOTO2024] Takemoto, K. (2024). The moral machine experiment on large language models. *Royal Society Open Science*, 11(2), 231393. https://doi.org/10.1098/rsos.231393. *arXiv*:2309.05958.

[AHMAD2025] Ahmad, M. S. Z., & Takemoto, K. (2025). Large-scale moral machine experiment on large language models. *PLOS One*, 20(5), e0322776. https://doi.org/10.1371/journal.pone.0322776. *arXiv*:2411.06790.

[VIDA2024] Vida, K., Damken, F., & Lauscher, A. (2024). Decoding multilingual moral preferences: Unveiling LLM's biases through the Moral Machine experiment. *Proceedings of AIES 2024*. *arXiv*:2407.15184.

[JIN2024] Jin, Z., et al. (2024). Language model alignment in multilingual trolley problems. *arXiv*:2407.02273.

### AI alignment and values

[OUYANG2022] Ouyang, L., Wu, J., Jiang, X., Almeida, D., et al. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems (NeurIPS 2022)*. *arXiv*:2203.02155.

[BAI2022] Bai, Y., Kadavath, S., Kundu, S., Askell, A., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv*:2212.08073.

[GABRIEL2020] Gabriel, I. (2020). Artificial intelligence, values, and alignment. *Minds and Machines*, 30, 411–437. https://doi.org/10.1007/s11023-020-09539-2. *arXiv*:2001.09768.

### LLM benchmarking and values

[CHIANG2024] Chiang, W.-L., et al. (2024). Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference. *arXiv*:2403.04132.

[LIANG2023] Liang, P., Bommasani, R., Lee, T., et al. (2023). Holistic evaluation of language models. *Transactions on Machine Learning Research*. *arXiv*:2211.09110.

[SANTURKAR2023] Santurkar, S., Durmus, E., Ladhak, F., Lee, C., Liang, P., & Hashimoto, T. (2023). Whose opinions do language models reflect? *Proceedings of ICML 2023*. *arXiv*:2303.17548.

[KIRGIS2024] Kirgis, P. (2024). Differences in the moral foundations of large language models. *arXiv*:2511.11790.

[HARTMANN2023] Hartmann, J., Schwenzow, J., & Witte, M. (2023). The political ideology of conversational AI: Converging evidence on ChatGPT's pro-environmental, left-libertarian orientation. *arXiv*:2301.01768.

[LLM-POLITICS] Dabadie, R., & Combes, A. (2024). The Political Gap Between AIs and Citizens. Foaster. https://llm-politics.foaster.ai / https://github.com/Foaster-ai/The_Political_Gap_Between_AIs_and_Citizens

[WEREWOLF] Dabadie, R., & Combes, A. (2024). Werewolf Benchmark: Evaluating LLM Social Reasoning Through Adversarial Deduction. Foaster. https://werewolf.foaster.ai / https://github.com/Foaster-ai/Werewolf-bench

### Gender bias in AI

[KOTEK2023] Kotek, H., Dockum, R., & Sun, D. Q. (2023). Gender bias and stereotypes in large language models. *Proceedings of Collective Intelligence Conference (CI '23)*. https://doi.org/10.1145/3582269.3615599. *arXiv*:2308.14921.

[WAN2023] Wan, Y., Pu, G., Sun, J., Garimella, A., Chang, K.-W., & Peng, N. (2023). "Kelly is a warm person, Joseph is a role model": Gender biases in LLM-generated reference letters. *Findings of ACL: EMNLP 2023*. *arXiv*:2310.09219.

[GEMINI-BIAS] Vincent, J. (2024, February 21). Google pauses Gemini's ability to generate images of people after historical inaccuracies. *The Verge*. https://www.theverge.com/2024/2/21/24079371/google-ai-gemini-generative-inaccurate-historical

### Cross-cultural psychology

[HENRICH2010] Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest people in the world? *Behavioral and Brain Sciences*, 33(2–3), 61–83. https://doi.org/10.1017/S0140525X0999152X

[HAIDT2001] Haidt, J. (2001). The emotional dog and its rational tail: A social intuitionist approach to moral judgment. *Psychological Review*, 108(4), 814–834. https://doi.org/10.1037/0033-295X.108.4.814

### Embodied AI and robotics

[BROHAN2023] Brohan, A., et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. *arXiv*:2307.15818.

[DRIESS2023] Driess, D., et al. (2023). PaLM-E: An Embodied Multimodal Language Model. *arXiv*:2303.03378.

[PALIGEMMA] Beyer, L., et al. (2024). PaliGemma: A versatile 3B VLM for transfer. *arXiv*:2407.07726.
