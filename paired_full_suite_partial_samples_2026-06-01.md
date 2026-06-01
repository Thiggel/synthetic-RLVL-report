# Paired Full-Suite Partial Sample Audit - 2026-06-01 02:45 CEST

Scope inspected: replacement eval `3682449` rows `0..21`, all from `official_igsm`.

Artifacts present at inspection time:

- `22` pass@k JSONs and `22` sample JSONLs in `${WORK}/synthetic-RLVL/passk_eval/paired_full_suite_sparse_20260528/`.
- Three-seed complete slices: `official_igsm` logic train-1-to-5/10/15/20 and `nl_exact` train-1-to-5/10/15.
- Partial slice: `official_igsm` `nl_exact` train-1-to-20 seed `3407`.
- `maze_navigation` and hard `attribute_constraints` still have no eval JSONs.

Metric summary:

- Logic train-1-to-5/10/15/20 OOD correct@16: `0.312/0.507/0.546/0.536`.
- Logic train-1-to-5/10/15/20 OOD internal-joint@16: `0.255/0.377/0.392/0.245`.
- Logic train-1-to-5/10/15/20 depth-50 correct@16: `0.240/0.458/0.542/0.510`.
- Logic train-1-to-5/10/15/20 depth-50 internal-joint@16: `0.177/0.281/0.292/0.219`.
- NL train-1-to-5/10/15 OOD correct@16: `0.366/0.589/0.618`; train-1-to-20 seed-3407 OOD correct@16 is `0.589`.
- NL train-1-to-5/10/15 depth-50 correct@16: `0.333/0.490/0.521`; train-1-to-20 seed-3407 depth-50 correct@16 is `0.594`.
- NL parse and translated joint validity remain `0.000` for all completed `nl_exact` rows.

Sample-generation findings:

- Logic samples use the intended `<formal>` wrapper, equation premises, cited proof lines, `<conclusion>`, and final `<answer>`. Answer extraction matches the final answer tag in inspected shallow, train-depth, and depth-50 cases.
- Shallow logic examples can be citation-free valid. For iGSM, `citation_free_grounded_valid` remains mostly unusable beyond trivial retrieval because generated variable names and arithmetic-substitution citations do not reliably align with the canonical grounded checker.
- Logic train-1-to-20 samples include correct train-depth and depth-50 answers, but depth-50 also has answer-wrong and proof-invalid cases; this supports keeping the partial readout diagnostic rather than final.
- NL samples use the intended `<think>` wrapper and final `<answer>`, and answer extraction works. Generated traces are readable iGSM-style arithmetic reasoning, but the current NL-to-logic translator does not parse them, so translated validity metrics remain blocked.
- Depth-50 NL samples can be answer-correct, but failures are also common and preserve normal format while deriving the wrong final numeric answer.

Interpretation guardrail:

Use the partial iGSM readout as provisional answer-correctness plus internal-logic-validity evidence only. Do not make paired-family NL-vs-logic validity claims until translator coverage and grounded iGSM validity are fixed or explicitly scoped out.
