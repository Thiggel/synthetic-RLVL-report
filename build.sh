#!/usr/bin/env bash
# Build from the repository root so that figure paths resolve.
set -e
cd "$(dirname "$0")"
export BIBINPUTS="./iclr2027:${BIBINPUTS:-}"
export BSTINPUTS="./iclr2027:${BSTINPUTS:-}"
rm -f main.aux main.bbl main.blg
pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true
bibtex main >/dev/null 2>&1 || true
pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true
pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true
echo "undefined: $(grep -c undefined main.log || echo 0)"
grep -E "Output written" main.log | tail -1
