# synthetic-RLVL-report

Reader-facing LaTeX reports for the synthetic-RLVL formal-logic CoT project.

Overleaf renders the ICLR 2027 draft by default:

- `main.tex` is the Overleaf entrypoint and loads `iclr2027/main.tex`.
- `iclr2027/main.tex` is the canonical anonymous conference manuscript built
  from the official ICLR 2027 style files published on July 28, 2026.
- `informal_report/main.tex` is the older generated informal report.
- `official_preprint/main_pre_iclr_2026-08-04.tex` preserves the previous root
  preprint source.
- `official_preprint/main_overleaf_2026-08-04-1340.tex` preserves the edited
  preprint from the manually merged Overleaf synchronization branch.
- `official_preprint/` contains template assets, the bibliography, the reproducible figure script, figures, and an archived placeholder `main.tex`. Do not use `official_preprint/main.tex` as the main document unless it is deliberately refreshed.
- `latexmkrc` selects XeLaTeX for the root preprint because the sans-serif font is bundled as Poppins under `official_preprint/fonts/poppins/`.

Overleaf does not automatically compile whichever `.tex` tab is currently open.
Use Overleaf's **Menu -> Main document** selector to switch between
`main.tex`, `iclr2027/main.tex`, and `informal_report/main.tex` when needed. The root and informal files include
`% !TeX root` comments for editors that honor them.

The experiment/code repo is expected at:

```bash
../synthetic-RLVL
```

Build locally when TeX is available:

```bash
make
```

The informal subdirectory mirrors the generated report bundle from:

```bash
../synthetic-RLVL/analysis/logic_cot_report_2026-05-25/
```

The repository should contain:

- `main.tex` for the ICLR draft entrypoint; report generation must not overwrite it
- `informal_report/main.tex` for the generated informal report
- `figures/` with all generated PDF/PNG figures referenced by the report
- `tables/` with all generated CSV result tables
- Markdown supplements with full/sample generations

Raw eval JSON, checkpoints, and Slurm logs stay in the experiment repo or `$WORK`.
