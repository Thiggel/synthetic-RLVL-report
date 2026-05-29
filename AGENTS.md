# AGENTS.md

This repo is the reader-facing ongoing LaTeX report for the synthetic-RLVL project.
The experiment/code repo is expected at `../synthetic-RLVL`.

## Report Discipline

- Keep `main.tex` and `sections/` as the polished report source.
- Pull current operational state from `../synthetic-RLVL/docs/current_system_state.md`.
- Pull live job state from `../synthetic-RLVL/docs/running_experiments.md`.
- Pull planned experiments from `../synthetic-RLVL/docs/experiment_backlog.md`.
- Pull selected stable figures/tables from `../synthetic-RLVL/analysis/logic_cot_report_2026-05-25/` only when they are needed by the LaTeX report.
- Do not copy bulky raw eval outputs or transient job artifacts into this repo.

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
