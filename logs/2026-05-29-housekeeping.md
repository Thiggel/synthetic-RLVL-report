# 2026-05-29 Housekeeping

- Established this repo as the ongoing reader-facing LaTeX report location.
- Kept the experiment repo handoff split into `current_system_state.md`,
  `running_experiments.md`, and `experiment_backlog.md`.
- Added the Slurm housekeeping rule to check freer compatible partitions and
  use `scontrol update JobId=<jobid> Partition=<partition1,partition2>` when safe.
- Left large/generated artifacts in the experiment repo unless selected for the
  report.
- Cleaned disposable experiment-repo artifacts: Python caches, old tracked
  smoke/probe materializations, and old Slurm logs. Kept logs for active job IDs
  and did not delete active `$WORK` checkpoints.
- Checked pending jobs against available partitions. Pending active jobs were
  waiting on array throttles, dependencies, or begin times, so no safe
  partition edit was applied.
- Verification: report `git diff --check` passed. TeX compilation was not run
  because `latexmk` and `pdflatex` are not installed on this node.
- After user clarification, replaced the lean scaffold with a full mirror of
  `../synthetic-RLVL/analysis/logic_cot_report_2026-05-25/`, including
  `main.tex`, all report figures, all CSV tables, and Markdown sample
  supplements.
