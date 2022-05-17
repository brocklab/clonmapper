#!/usr/bin/env python3

import csv
import sys
from pathlib import Path

WIDTH_CUTOFF = int(round(94 / 2, 0))


def main():

    path_to_csv = Path.cwd() / sys.argv[1]
    path_to_tex = Path.cwd() / sys.argv[2]
    caption = sys.argv[3]

    rows = []

    # get header and row information from csv
    with path_to_csv.open(mode="r") as f:
        reader = csv.DictReader(f)
        # column_fmt = '|'.join(['c']*len(reader.fieldnames))
        column_fmt = "c l p{{.67\\textwidth}} l"
        headers = [rf"\textbf{{{header}}}" for header in reader.fieldnames]
        header_str = " & ".join(headers) + r" \\"

        for row in reader:
            # split sequences so they will wrap nicer in the table
            row_str = (
                " & ".join(
                    [
                        v
                        if len(v) < WIDTH_CUTOFF
                        else "-".join([v[:WIDTH_CUTOFF], v[WIDTH_CUTOFF:]])
                        for v in row.values()
                    ]
                )
                + r" \\"
                + "\n"
            )
            # row_str = ' & '.join(row.values())+ r' \\' +'\n'
            rows.append(row_str)

        rows = "".join(rows)

    table_tex_str = rf"""
%...
% generated using latex_table.py

% DO NOT edit manually, regenerate with: snakemake table
\setlength{{\tabcolsep}}{{0.5em}} % for the horizontal padding
{{\renewcommand{{\arraystretch}}{{1.2}} % for the vertical padding
\begin{{table}}[ht!]
  \begin{{center}}
    \begin{{adjustbox}}{{width=\textwidth}}
      \label{{tab:table1}}
      \begin{{tabular}}{{{column_fmt}}}
      \hline
        {header_str}
      \hline
        {rows}
      \hline
      \end{{tabular}}
    \end{{adjustbox}}
    \caption{{{caption}}}
  \end{{center}}
\end{{table}}
}}
%...
"""
    # build latex file
    path_to_tex.parent.mkdir(exist_ok=True)

    with path_to_tex.open(mode="w") as f:
        f.write(table_tex_str)


if __name__ == "__main__":
    main()