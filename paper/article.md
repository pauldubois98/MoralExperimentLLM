# Do Large Language Models Share Human Moral Values? Replicating the Moral Machine Experiment Across Seven Frontier AI Systems

**Paul Dubois**

---

## Abstract

The Moral Machine experiment collected over 40 million human responses to trolley-problem-style autonomous vehicle dilemmas across 130 countries, revealing systematic cross-cultural variation in moral preferences along nine dimensions.
This study replicates this experiment with seven frontier large language models (LLMs): Claude Opus 4.7, GPT-5.5, Gemini 3 Pro, Mistral Large 3, Grok 4.1, DeepSeek v4 Pro, and Llama 4 Maverick.
The Average Marginal Causal Effects (AMCEs) was computed using the original paper's weighted OLS regression methodology.
The results show that LLMs occupy a distinct region of moral space: all seven fall outside the main human country clusters in a PCA of the nine-dimensional AMCE profile space, suggesting that current models are not well-aligned with the distribution of human moral preferences even on well-structured dilemmas.
At the same time, models differ substantially from one another, raising practical questions about whose values should govern AI systems deployed in safety-critical contexts.
This study further finds that modifying the prompt produces negligible changes in AMCE estimates.
The response length varies by an order of magnitude across models despite broadly similar preference profiles among the three most widely deployed systems.

---

## 1. Introduction

As autonomous vehicles, surgical robots, and other safety-critical systems increasingly incorporate AI decision-making, the question of whether AI systems share human moral intuitions becomes practically consequential.
A self-driving car that must choose between hitting a group of pedestrians or swerving into its own passengers cannot defer the decision; some preference ordering must be encoded, implicitly or explicitly, in its behaviour.

The Moral Machine experiment [AWAD2018] provided the largest empirical dataset of human moral preferences, asking millions of participants across 130 countries to judge unavoidable accident scenarios involving an autonomous vehicle.
The study identified nine binary moral dimensions: intervention, relation to the vehicle, legality of crossing, gender, physical fitness, social status, age, number of lives, and species.
The study found that aggregate human preferences, quantified as Average Marginal Causal Effects, vary substantially across cultural clusters while sharing a common core (strong preference for saving humans over animals, more lives over fewer, and legal pedestrians over illegal ones).

The rapid deployment of large language models in agentic and embodied settings [BROHAN2023, DRIESS2023] including robotics platforms capable of physical action makes the question of LLM moral alignment newly urgent.
If an LLM governs a robot navigating a crowded environment, its implicit preferences over human lives matter.
Yet surprisingly little is known about whether the moral profiles of current frontier models resemble those of humans, and how much models differ from one another.

This study asks three questions:

1. **Alignment**: Do frontier LLMs display moral preferences similar to those of the human global average?
2. **Diversity**: Do different LLMs differ meaningfully from one another in their moral profiles?
3. **Prompt sensitivity**: Does instructing a model to reason carefully before deciding ("emphasis" prompting) change its moral preferences?

Following the broader effort to benchmark LLMs along non-capability dimensions including user preference rankings [CHIANG2024], political orientation [LLM-POLITICS], and social reasoning in adversarial settings [WEREWOLF] this work proposes moral preference profiling as a complementary axis for understanding frontier AI systems.

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

### 2.4 AMCE computation

Following [AWAD2018], nine Average Marginal Causal Effects were computed per model using weighted ordinary least squares with inverse-probability weights.
The nine AMCEs quantify the change in probability of a group being saved when the relevant attribute shifts from its baseline to its target value (e.g., from illegal crossing to legal crossing for the Legality dimension).
Confidence intervals were computed as ±1.96 SE.

For analyses combining both prompt variants, AMCE estimates and standard errors were averaged across the two variants per model.
The human global average baseline was computed from the 130-country dataset of [AWAD2018] by averaging country-level estimates.

---

## 3. Results

### 3.1 STAY vs. SWERVE baseline rates

Before examining the nine moral dimensions, all seven models swerve (intervene) at substantially higher rates than a random baseline, ranging from roughly 60% to over 90% SWERVE across models (Figure 1).
Llama 4 Maverick exhibits the highest intervention rate; Mistral Large 3 the lowest among the seven.

![STAY vs SWERVE rates by model](../figures/fig1_stay_swerve.png)
*Figure 1. Proportion of STAY vs. SWERVE decisions per model, averaged across both prompt variants.*

### 3.2 AMCE profiles: LLMs vs. the human global average

Figure 2 shows the forest plot of AMCE estimates for all nine dimensions, comparing each model to the human global average.

![AMCE forest plot](../figures/fig5a_amce_forest.png)
*Figure 2. Average Marginal Causal Effects for nine moral dimensions across all seven LLMs and the human global average (averaged across standard and emphasis variants). Positive values indicate preference for the right-side group; error bars show 95% confidence intervals.*

The key findings are summarised dimension by dimension:

**Intervention (stay→swerve).** Humans show a weak preference for omission over commission (AMCE = +0.05, favouring swerving only marginally). All seven LLMs show a much stronger intervention preference, ranging from +0.13 (Mistral) to +0.66 (Llama 4 Maverick). Llama 4 Maverick stands out as a strongly action-oriented model: it swerves in nearly two-thirds more cases than baseline regardless of outcome composition.

**Relation to AV (passengers→pedestrians).** Humans slightly prefer to spare pedestrians over passengers (AMCE = +0.10). Claude Opus 4.7 (+0.52) strongly prefers pedestrians. GPT-5.5 (+0.34) and Llama 4 Maverick (+0.23) follow. Grok 4.1 (+0.13) is close to human. Mistral Large 3 (−0.37) reverses the preference entirely, sparing its own passengers over pedestrians.

**Legality (illegal→legal).** Humans reward legal pedestrians (AMCE = +0.35). Claude (+0.57), GPT-5.5 (+0.61), and Gemini (+0.61) substantially amplify this preference. Grok (+0.21) and DeepSeek (+0.27) are attenuated but positive. Mistral (−0.45) and Llama 4 Maverick (−0.25) invert it, favouring illegal crossers a striking reversal of the human norm.

**Gender (male→female).** Humans display a moderate preference for saving women (AMCE = +0.12). All LLMs show near-zero gender preference (range: −0.07 to +0.07), effectively gender-neutral. This likely reflects deliberate alignment choices by developers to avoid reinforcing gender stereotypes, applied broadly enough to suppress gender preferences even in emergency contexts where human intuitions diverge (see Section 4.3).

**Fitness (large→fit).** Humans mildly prefer fitter individuals (AMCE = +0.15). Most LLMs match this closely (range: +0.04 to +0.16), with Mistral (−0.12) being the exception.

**Social status (low→high).** Humans show a modest preference for high-status individuals (AMCE = +0.35), though this varies widely across cultural clusters. All LLMs show near-zero social status preference (range: −0.14 to +0.18), consistent with egalitarian alignment training.

**Age (elderly→young).** Humans strongly prefer to save younger people (AMCE = +0.48). Gemini 3 Pro (+0.46) closely matches the human average. Claude (+0.27) is intermediate. GPT-5.5 (+0.05), Grok (+0.06), DeepSeek (+0.04), and Llama 4 Maverick (+0.05) are nearly indifferent to age. Mistral (−0.18) slightly prefers the elderly.

**Number of lives (fewer→more).** Humans prefer to save more lives (AMCE = +0.49). This is the dimension of strongest and most consistent LLM agreement with human preferences, though several models overshoot dramatically: GPT-5.5 (+0.98), Grok 4.1 (+1.00), and Llama 4 Maverick (+1.00) reach near-perfect utilitarian maximisation. Claude (+0.73) and Mistral (+0.70) are more moderate.

**Species (pets→humans).** Humans strongly prefer humans over animals (AMCE = +0.57). GPT-5.5, Gemini, and Grok reach the theoretical maximum (+1.00). Claude (+0.87) and DeepSeek (+0.90) are strong but below ceiling. Mistral (−0.01) and Llama 4 Maverick (+0.08) are near-indifferent to species Mistral being the only model that does not reliably prefer humans over animals.

Figure 3 shows the same preferences as a radar chart for visual comparison.

![Radar chart of AMCE dimensions](../figures/fig5c_radar.png)
*Figure 3. Radar chart of AMCE estimates across all nine dimensions. The dashed line shows the human global average.*

Figures 4 and 5 display the six character-attribute dimensions as a heatmap and per-attribute bar charts.

![Preference heatmap](../figures/fig2_preference_heatmap.png)
*Figure 4. Heatmap of moral preferences across six character-type dimensions (Δ Pr from 0.5). Positive (blue) = preference for the right-side group; negative (red) = preference for the left-side group.*

![Per-attribute bar chart](../figures/fig3_per_attribute.png)
*Figure 5. Per-attribute moral preferences for all seven LLMs across the six character-type scenario dimensions.*

### 3.3 Moral distance map: PCA of nine-dimensional profiles

To place LLM profiles relative to the 130-country human distribution, PCA was performed on the country-level AMCE matrix from [AWAD2018] and projected each LLM into the same space (Figure 6).

![PCA moral distance map](../figures/fig5b_pca_map.png)
*Figure 6. PCA of nine-dimensional AMCE profiles for 130 countries (coloured by cluster: Western, Eastern, Latin/Southern) with LLMs overlaid. All seven LLMs fall outside the main human clusters.*

All seven LLMs fall outside the three main human cultural clusters.
The nearest country for each model (by Euclidean distance in the original nine-dimensional AMCE space) is:

| Model | Nearest country |
|---|---|
| Claude Opus 4.7 | Jordan |
| GPT-5.5 | Denmark |
| Gemini 3 Pro | Denmark |
| Mistral Large 3 | Brazil |
| Grok 4.1 | Pakistan |
| DeepSeek v4 Pro | Pakistan |
| Llama 4 Maverick | Jersey |

This finding is striking: despite all models having been developed by companies based in the United States, Europe, and China and trained predominantly on English-language data, their moral profiles do not cluster near any major human population in the PCA space.
The divergence from the human distribution suggests that standard RLHF alignment processes do not systematically instil the moral preferences of any particular human population.

### 3.4 Inter-model diversity

The variation among models is comparable in magnitude to the variation across human cultural clusters.
Mistral Large 3 inverts the human preference on four dimensions (Legality, Relation to AV, Age, and Gender), while Llama 4 Maverick shows the highest intervention bias of any model tested, paired with near-indifference to species.
GPT-5.5 and Gemini 3 Pro converge closely, both mapping to Denmark and displaying similar profiles (near-ceiling on Species and No. of Lives, moderate on intervention).
This inter-model diversity has a concrete implication: the choice of LLM vendor for an autonomous system is not morally neutral, and could lead to systematically different decisions in rare but consequential edge cases.

### 3.5 Effect of emphasis prompting

Comparing standard and emphasis prompt variants (Figures 7 and 8) reveals that prompting style has minimal effect on AMCE estimates for the three most widely deployed models (Claude, GPT-5.5, Gemini).
Some variation is visible for Mistral, Grok, and Llama 4 Maverick notably Mistral's Social Status estimate shifts by +0.13 points under emphasis prompting but no dimension shows a reversal of sign for any mainstream model.

![AMCE delta heatmap](../figures/fig6a_prompt_delta_heatmap.png)
*Figure 7. Heatmap of AMCE differences (emphasis − standard) per model and dimension. Near-zero entries (white) indicate prompt-invariant preferences.*

![Standard vs emphasis forest plot](../figures/fig6b_prompt_forest.png)
*Figure 8. Side-by-side AMCE estimates for standard (filled circle) and emphasis (open square) variants per model.*

This stability suggests that the moral preferences captured here are robust properties of model weights rather than surface-level response styles that vary with framing.

### 3.6 Response length and latency

Response length varies substantially across models (Figure 9).
Gemini 3 Pro produces the longest responses (median 913 tokens combined across variants), while GPT-5.5 is the most concise (median 164 tokens).
Importantly, response length shows no meaningful variation across the seven scenario types (Figure 10), indicating that models do not deliberate more on any particular moral dimension than others.

![Token distribution](../figures/fig7a_token_distribution.png)
*Figure 9. Output token distribution by model (standard + emphasis combined). Violin shows density; box shows quartiles.*

![Token count by scenario type](../figures/fig7c_length_by_factor.png)
*Figure 10. Median output tokens by scenario type. No systematic variation is observed across moral dimensions, for any model.*

Emphasis prompting increases response length for all models (Figure 11), consistent with the instruction to think before answering yet this additional reasoning does not translate into different preferences (Section 3.5).

![Standard vs emphasis token comparison](../figures/fig7b_emphasis_vs_standard.png)
*Figure 11. Output token counts for standard (lighter) vs. emphasis (darker) prompt variants per model.*

Latency varies substantially across providers (Figure 12).
Given that the three mainstream models display broadly similar moral profiles, response speed becomes a primary differentiating factor for deployment in time-sensitive contexts in this light, GPT-5.5's combination of short responses and low latency is noteworthy.

![Latency CDF](../figures/fig7d_latency.png)
*Figure 12. Cumulative distribution of response latency by model.*

---

## 4. Discussion

### 4.1 LLMs are morally out-of-distribution relative to humans

The most robust finding of this study is that no tested LLM sits within the main human cultural clusters on the PCA moral map, despite all being trained primarily on human-generated content.
This out-of-distribution result is consistent with the hypothesis that RLHF and related alignment techniques do not faithfully reproduce the moral preferences of any human population, but rather create a novel moral profile that prioritises certain values (high utilitarian weight on number of lives, near-universal human-over-animal preference) while discarding others (age preference, gender preference) that are robustly present in human data.
Whether this constitutes a bug or a feature depends on normative commitments: one might argue that LLMs have corrected for biases present in human moral intuitions, or that they have drifted from the values of the populations they are meant to serve.

### 4.2 Substantial inter-model diversity raises deployment questions

The diversity among LLMs is surprising.
One might expect models trained on overlapping datasets and aligned with similar constitutional principles to converge on similar moral profiles.
Instead, Mistral and Llama 4 Maverick display profiles that partially invert human norms, while GPT-5.5 and Grok 4.1 display near-ceiling utilitarian preferences on Species and No. of Lives that no human population approaches.

This heterogeneity has a practical implication that goes beyond academic interest.
Unlike human drivers, who show broadly similar moral intuitions regardless of the car manufacturer, AI-powered vehicles could introduce model-brand-level moral heterogeneity into public space.
In a future where LLMs govern autonomous systems operating in public environments, the choice of AI provider is equivalent to a choice of moral framework.
This concern is not hypothetical: LLMs are already deployed in robotics platforms capable of physical manipulation [BROHAN2023, DRIESS2023, PALIGEMMA], and the extension to autonomous vehicles is architecturally straightforward.

### 4.3 Gender neutrality as an alignment artefact

The near-universal gender indifference among LLMs all show AMCEs within ±0.07 on the Gender dimension, versus +0.12 for the human average is best understood as a consequence of deliberate alignment choices rather than an independent moral stance.
Developers have invested significant effort in making models gender-neutral in content generation to correct for historical biases in training data (e.g., the tendency to assign male gender to professional roles).
This correction appears to generalise to moral reasoning contexts, suppressing the modest human preference for saving women that emerges consistently across cultures in the Moral Machine data [GEMINI-BIAS].
Whether this generalisation is desirable is an open question: in structured dilemma contexts, gender neutrality differs from human norms but may reflect a principled commitment to equality that humans endorse in the abstract even if not in the moment.

### 4.4 Emphasis prompting does not change moral preferences

The finding that emphasis prompting does not materially alter AMCE estimates is reassuring for practitioners but raises theoretical questions.
It suggests that moral preferences are encoded as relatively stable properties of model weights rather than as context-sensitive response strategies.
Emphasis prompting consistently elicits longer responses models generate more text when asked to reason carefully but this additional text does not correspond to changed decisions.
From a deployment standpoint, this implies that simple prompt engineering is unlikely to be an effective tool for adjusting LLM moral profiles, and that aligning a model's moral preferences with a target population would require retraining or fine-tuning.

### 4.5 Parse failures as a reliability concern

A small fraction of responses across all models could not be parsed as valid STAY/SWERVE choices.
In deployed systems, such failures would lead to undefined behaviour a meaningful safety concern.
All 20 GPT-5.5 parse failures in the standard run were caused by API-side token truncation at exactly 512 tokens, indicating a configuration issue rather than a model-level failure; these were successfully resolved on rerun.
Engineers deploying LLMs in safety-critical decision pipelines should implement robust output validation and fallback logic, and monitor parse failure rates as a reliability metric.

### 4.6 Limitations

This study has several limitations.
First, all scenarios were presented in English; moral preferences may shift in other languages [AWAD2018].
Second, temperature was set to zero for reproducibility, but some models may exhibit different preferences at higher temperatures.
Third, the Moral Machine paradigm, while widely validated, abstracts away many real-world complexities of autonomous driving.
Fourth, the emphasis and standard prompts differ in only one sentence; more substantial prompt variations (e.g., role assignment, explicit ethical frameworks) may produce larger effects.
Finally, model weights change over time through fine-tuning updates; the profiles reported here reflect model states as of May 2026.

### 4.7 Conclusion

Frontier LLMs exhibit consistent and distinct moral preferences that diverge from the human global average on multiple dimensions, differ substantially from one another, and remain stable under prompt variation.
These findings suggest that the implicit moral profiles of current AI systems are neither well-calibrated to human values nor uniform across providers a combination that warrants careful consideration as LLMs are increasingly deployed in systems with real-world consequences for human welfare.

---

## References

[AWAD2018] Awad, E., Dsouza, S., Kim, R., Schulz, J., Henrich, J., Shariff, A., Bonnefon, J.-F., & Rahwan, I. (2018). The Moral Machine experiment. *Nature*, 563, 59–64. https://doi.org/10.1038/s41586-018-0637-6

[BROHAN2023] Brohan, A., et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. *arXiv*:2307.15818.

[DRIESS2023] Driess, D., et al. (2023). PaLM-E: An Embodied Multimodal Language Model. *arXiv*:2303.03378.

[PALIGEMMA] Beyer, L., et al. (2024). PaliGemma: A versatile 3B VLM for transfer. *arXiv*:2407.07726.

[CHIANG2024] Chiang, W.-L., et al. (2024). Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference. *arXiv*:2403.04132.

[LLM-POLITICS] *(TODO: find citation for llm-politics.foaster.ai)*

[WEREWOLF] *(TODO: find citation for werewolf.foaster.ai)*

[GEMINI-BIAS] Vincent, J. (2024, February 21). Google pauses Gemini's ability to generate images of people after historical inaccuracies. *The Verge*. https://www.theverge.com/2024/2/21/24079371/google-ai-gemini-generative-inaccurate-historical
