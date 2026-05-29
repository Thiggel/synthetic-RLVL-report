# AGENTS.md

This repo is the reader-facing ongoing LaTeX report for the synthetic-RLVL project.
The experiment/code repo is expected at `../synthetic-RLVL`.

## Report Discipline

- Mirror the full generated report bundle from `../synthetic-RLVL/analysis/logic_cot_report_2026-05-25/`.
- `main.tex` should be copied from `../synthetic-RLVL/analysis/logic_cot_report_2026-05-25/logic_cot_report_2026-05-25.tex`.
- `figures/` should contain all generated report figures, including PDFs referenced by `main.tex` and PNG copies.
- `tables/` should contain all generated CSV result tables.
- Copy Markdown generation supplements from the generated report root.
- Do not copy raw eval JSON, checkpoints, transient Slurm logs, or `$WORK` checkpoint artifacts into this repo.

## Push Discipline

- After changing the report, commit and push this repo to GitHub when network/authentication permits.
- Remote: `git@github.com:Thiggel/synthetic-RLVL-report.git`.
- If TeX tooling is unavailable, still update the sources and mention that compilation was not run.

## Slurm Housekeeping Note

Slurm jobs are managed in `../synthetic-RLVL`, not here. When updating report
status from pending jobs, also check whether compatible freer partitions could
reduce wait time. If safe, update the experiment repo handoff after running:

```bash
scontrol update JobId=<jobid> Partition=<partition1,partition2>
```
