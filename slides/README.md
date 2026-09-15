# Slide assets

`results_overview.pdf` and `results_overview-1.png` hold every finished
benchmark for the dose sweep, grouped by benchmark family, with the best cell
of each row in bold. Three seeds per condition except the 25 percent columns,
which have one. Multi-hop rows are rescored from the saved samples with the
stop strings the task files originally lacked. Code rows are incomplete while
the remaining jobs run.

Rebuild after new results land:

    ssh alex '/home/vault/c107fa/c107fa12/.venv_rlvl_posttrain/bin/python /tmp/overview_table.py' \
      > slides/results_overview_table.tex
    cd slides && pdflatex results_overview.tex && pdftoppm -r 200 -png results_overview.pdf results_overview

The generator lives in `scripts/analysis/overview_table.py` of the code repo.
