# synthetic-RLVL-report

Reader-facing LaTeX reports for the synthetic-RLVL formal-logic CoT project.

Overleaf should render the official preprint by default:

- `main.tex` is the official preprint entrypoint.
- `informal_report/main.tex` is the older generated informal report.
- `official_preprint/` contains the preprint source copy, template assets, bibliography, and reproducible figure script.

Overleaf does not automatically compile whichever `.tex` tab is currently open.
Use Overleaf's **Menu -> Main document** selector to switch between
`main.tex` and `informal_report/main.tex` when needed. Both files include
`% !TeX root` comments for editors that honor them.

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

- `main.tex` for the official preprint
- `informal_report/main.tex` for the generated informal report
- `figures/` with all generated PDF/PNG figures referenced by the report
- `tables/` with all generated CSV result tables
- Markdown supplements with full/sample generations

Raw eval JSON, checkpoints, and Slurm logs stay in the experiment repo or `$WORK`.
