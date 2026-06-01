# Paired Full-Suite Partial Sample Audit - 2026-06-01 18:32 CEST

Scope inspected: replacement eval `3682449` rows `0..33` where complete, plus targeted official-iGSM NL rerun `3689003` completed rows `3..5`, `9..11`, `15`, and `16`.

Artifacts present at inspection time:

- `31` pass@k JSONs and `31` sample JSONLs in `${WORK}/synthetic-RLVL/passk_eval/paired_full_suite_sparse_20260528/`.
- `official_igsm` has all `30/30` rows, with `8/15` `nl_exact` rows overwritten by the targeted translator rerun.
- `maze_navigation` has the first completed row: `nl_exact`, train-1-to-5, seed `3407`; rows `30..32` and `34` are still running, and rows `35..59` are throttle-pending.
- Hard `attribute_constraints` still has no eval JSONs.

Metric summary:

- Official-iGSM logic train-1-to-5/10/15/20/25 OOD correct@16: `0.312/0.507/0.546/0.536/0.488`.
- Official-iGSM logic train-1-to-5/10/15/20/25 OOD internal-joint@16: `0.255/0.377/0.392/0.245/0.106`.
- Official-iGSM `nl_exact` train-1-to-5/10/15/20/25 OOD correct@16 after the partial rerun state: `0.359/0.569/0.612/0.576/0.585`.
- Official-iGSM `nl_exact` OOD parser coverage@16 is now `1.000/1.000/0.664/0.000/0.000` for train-1-to-5/10/15/20/25 because the rerun has only covered train-1-to-5, train-1-to-10, and two train-1-to-15 seeds so far.
- Official-iGSM `nl_exact` translated joint@16 and translated validity@16 remain `0.000` on all current train ranges, including completed rerun rows.
- The first maze row (`nl_exact`, train-1-to-5, seed `3407`) has OOD correct@16 `0.088`, OOD NL parse@16 `0.000`, and depth-50 correct@16 `0.000`.

Sample-generation findings:

- Logic samples use the intended `<formal>` wrapper, equation premises, cited proof lines, `<conclusion>`, and final `<answer>`. Answer extraction matches the final answer tag in inspected shallow, train-depth, and depth-50 cases.
- Shallow logic examples can be citation-free valid. For iGSM, `citation_free_grounded_valid` remains mostly unusable beyond trivial retrieval because generated variable names and arithmetic-substitution citations do not reliably align with the canonical grounded checker.
- Logic train-1-to-20 samples include correct train-depth and depth-50 answers, but depth-50 also has answer-wrong and proof-invalid cases; this supports keeping the partial readout diagnostic rather than final.
- Rerun iGSM NL samples use the intended `<think>` wrapper and final `<answer>`, and answer extraction works. The translator now parses generated official-relation, substitution, and modulo-23 lines, but generated variable names often do not match the gold formal premises, so translated proof validity remains zero.
- The first maze NL samples use the intended `<think>` wrapper and answer extraction works on shallow cases, but the HFSA NL translator does not cover maze proof grammar; parser and translated-validity metrics are therefore zero. Deeper maze samples frequently run long and hit max-token limits in active logs, so the first one-seed maze metric is only a diagnostic partial.

Interpretation guardrail:

Use the partial paired-family readout as provisional diagnostics only. Do not make paired-family NL-vs-logic validity claims until `3689003` finishes, non-iGSM eval rows complete, and family-specific translated-validity/grounding assumptions are explicitly scoped.
