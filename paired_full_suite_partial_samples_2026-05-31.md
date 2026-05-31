# Paired Full-Suite Partial Sample Audit - 2026-05-31 22:34 CEST

Scope inspected: replacement eval `3682449` rows `0..13`, all from `official_igsm`.

Artifacts present at inspection time:

- `14` pass@k JSONs and `14` sample JSONLs in `${WORK}/synthetic-RLVL/passk_eval/paired_full_suite_sparse_20260528/`.
- Three-seed complete slices: `official_igsm` train-1-to-5 and train-1-to-10 for both `logic` and `nl_exact`.
- Partial slice: `official_igsm` `logic` train-1-to-15 seeds `3407` and `3408`.

Metric summary:

- Logic train-1-to-5: OOD correct/internal-joint@16 `0.312/0.255`, depth-50 correct/internal-joint@16 `0.240/0.177`.
- Logic train-1-to-10: OOD `0.507/0.377`, depth-50 `0.458/0.281`.
- Logic train-1-to-15 partial: OOD `0.547/0.400`, depth-50 `0.562/0.344` over two seeds.
- NL train-1-to-5: OOD correct@16 `0.366`, depth-50 correct@16 `0.333`; translated joint and NL parse remain `0.000`.
- NL train-1-to-10: OOD correct@16 `0.589`, depth-50 correct@16 `0.490`; translated joint and NL parse remain `0.000`.

Sample-generation findings:

- Logic samples use the intended `<formal>` wrapper, equation premises, cited proof lines, `<conclusion>`, and final `<answer>`. Shallow depth-1 samples can be correct and grounded-valid.
- iGSM grounded validity is not currently usable as the main logic metric: depth-2 and deeper examples often have internally valid cited arithmetic proofs but `citation_free_grounded_valid=0.0`, matching the prior arithmetic-substitution/grounding caveat.
- NL samples use the intended `<think>` wrapper and final `<answer>`, and answer extraction works. The generated NL trace text is human-readable iGSM reasoning, but the current NL-to-logic translator does not parse it, so translated validity metrics remain `0.000`.
- Depth-50 samples are mixed: both modalities can still answer correctly, but logic traces often become long equation chains with invalid or ungrounded proof segments, and NL traces sometimes lose format or drift/truncate.

Interpretation guardrail:

Use the partial iGSM readout only as provisional answer-correctness plus internal-logic-validity evidence. Do not make paired-family NL-vs-logic validity claims until translator coverage and grounded iGSM validity are fixed or explicitly scoped out.
