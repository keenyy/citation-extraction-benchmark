# Citation extraction benchmark

`cases.csv` indexes the 250 judgments. It is not a citation list.

## Revised reference keys and pipeline

- [`answer_keys/`](answer_keys/) contains 250 TXT files, one per judgment. The revised keys contain 4,018 case citations and 627 academic references.
- Files `0000.txt` to `0249.txt` correspond to the zero-indexed data rows in `cases.csv`, excluding its header. Each file separates case citations from academic references.
- [`pipeline/`](pipeline/) contains the revised extraction source. [`regex_baseline.py`](regex_baseline.py) is unchanged. The source snapshot is not a standalone benchmark runner.

## Original reference CSV

`references.csv` is retained unchanged. Filter `source_type` to `case` for its 4,018 case citations or to `academic` for its 624 academic references. The original files and pipeline are preserved at [commit a3a84c7](https://github.com/keenyy/citation-extraction-benchmark/tree/a3a84c7419bdb474bda32e7c8947c82ab8ffa44a).
