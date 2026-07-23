# OLMo-3-32B conditioned-dual sample audit, 2026-07-01

Artifacts:

- Single-modality evals: `$HPCVAULT/synthetic-RLVL/passk_eval/hfsa_model_ablation_32b_train25_20260619/`
- Conditioned-dual evals: `$HPCVAULT/synthetic-RLVL/passk_eval/hfsa_conditioned_dual_olmo3_1125_32b_20260619/`
- All rows are train-1-to-25, 10k SFT steps, seeds 3407/3408/3409. Conditioned dual is a same-step mixed-exposure run, not an additive data/control run.

## Aggregate readout

Pass@16 by seed on the long-depth OOD band:

| run | seed | correct | relevant joint | format/parse |
| --- | ---: | ---: | ---: | ---: |
| single logic | 3407 | 0.956 | 0.562 | 1.000 |
| single logic | 3408 | 0.925 | 0.481 | 1.000 |
| single logic | 3409 | 0.981 | 0.388 | 1.000 |
| conditioned logic | 3407 | 0.925 | 0.500 | 1.000 |
| conditioned logic | 3408 | 0.988 | 0.525 | 1.000 |
| conditioned logic | 3409 | 0.975 | 0.438 | 1.000 |
| single NL | 3407 | 0.669 | 0.606 | 0.931 |
| single NL | 3408 | 0.738 | 0.706 | 0.950 |
| single NL | 3409 | 0.650 | 0.325 | 1.000 |
| conditioned NL | 3407 | 0.362 | 0.300 | 0.988 |
| conditioned NL | 3408 | 0.613 | 0.537 | 0.825 |
| conditioned NL | 3409 | 0.850 | 0.775 | 1.000 |

The conditioned-logic mean is slightly higher than single logic, but the effect is small. The conditioned-NL mean is lower because seeds 3407 and 3408 degrade, while seed 3409 improves over its single-modality counterpart. The NL drop is therefore high-variance interference/exposure, not a universal mode failure.

## Sample-surface checks

Matched stored sample prompts:

| mode | matched prompts | single-only | conditioned-only |
| --- | ---: | ---: | ---: |
| logic | 240 | 0 | 0 |
| NL | 240 | 0 | 0 |

Tag counts over the 240 stored samples per run:

| run | `<formal>` | `<think>` | `<proof>` | `<answer>` |
| --- | ---: | ---: | ---: | ---: |
| single logic | 240 | 0 | 235 | 235 |
| conditioned logic | 240 | 0 | 229 | 229 |
| single NL | 0 | 240 | 230 | 229 |
| conditioned NL | 0 | 240 | 233 | 234 |

There is no visible mode leakage: conditioned logic stays formal, and conditioned NL stays natural-language formatted.

## Matched sample outcomes

Correctness pairs are `(single, conditioned)` over exactly matched prompts:

| mode | all samples | step >= 26 | step >= 35 | step >= 45 |
| --- | --- | --- | --- | --- |
| logic | TT 161, FF 45, TF 23, FT 11 | FF 44, TF 17, FT 9, TT 8 | FF 40, TF 12, FT 6, TT 2 | FF 25, TF 4, FT 1 |
| NL | TT 182, FF 26, FT 19, TF 13 | FF 26, TT 20, FT 19, TF 13 | FF 26, FT 17, TF 13, TT 4 | FF 20, TF 5, FT 4, TT 1 |

The stored first-sample JSONLs are diagnostic only; Table 7 uses pass@16. They show that conditioned training creates both wins and losses on the same prompt distribution. At long depths, both modes mostly fail by choosing or continuing the wrong branch/state chain.

Representative pairs:

- NL single correct / conditioned wrong: seed 3407, step 35, gold `violet`. Single NL ends with `q is orchid; q is south; r is violet` and answers `violet`. Conditioned NL follows a different path ending `q is teal; q is west; r is ruby` and answers `ruby`.
- NL single wrong / conditioned correct: seed 3408, step 30, gold `ruby`. Single NL ends `l is olive; l is south; m is olive` and answers `olive`. Conditioned NL ends `l is willow; l is west; m is ruby` and answers `ruby`.
- Logic single wrong / conditioned correct: seed 3407, step 25, gold `ivory`. Single logic concludes `Ih` and answers `ruby`; conditioned logic concludes `Ah` and answers `ivory`.
- Logic single correct / conditioned wrong: seed 3407, step 25, gold `laurel`. Single logic concludes `Th` and answers `laurel`; conditioned logic concludes `Fh` and answers `birch`.

Interpretation: the 32B result supports a capacity-dependent benefit of mixed-mode supervision for the formal prompted mode. It does not show that formal supervision improves the NL prompted mode. The NL mode is more verbose and higher-entropy, and under the same 10k-step budget each modality receives less direct same-surface exposure than in the single-modality baselines.
