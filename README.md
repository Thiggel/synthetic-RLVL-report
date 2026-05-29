# synthetic-RLVL-report

Reader-facing ongoing LaTeX report for the synthetic-RLVL formal-logic CoT project.

The experiment/code repo is expected at:

```bash
../synthetic-RLVL
```

Build locally when TeX is available:

```bash
make
```

This repo mirrors the full generated report bundle from:

```bash
../synthetic-RLVL/analysis/logic_cot_report_2026-05-25/
```

It should contain:

- `main.tex`
- `figures/` with all generated PDF/PNG figures referenced by the report
- `tables/` with all generated CSV result tables
- Markdown supplements with full/sample generations

Raw eval JSON, checkpoints, and Slurm logs stay in the experiment repo or `$WORK`.
