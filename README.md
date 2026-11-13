# Fertility and Reproduction in U.S. Historical Newspapers, 1840–1923

How did U.S. newspapers discuss fertility, reproduction, and population between
1840 and 1923? This project shares two workflows from the initial exploration
of a paper in progress. The goal was to assess corpus coverage and identify
changes in vocabulary worth investigating through close reading.

## Corpus and approach

The research corpus contains selected historical newspaper records with
source references to the Library of Congress. Archive coverage, search
criteria, OCR quality, and repeated text can affect which material appears
in the corpus. The research corpus and paper results are private. The example
CSV contains fictional text and metadata created to demonstrate the workflow.

- `audit_corpus.py` summarizes coverage by decade and by state and reports
  repeated cleaned text, identifiers, and source blocks when available.
  Repeated records are retained. A text can appear more than once because
  of republication or because of how the corpus was assembled.
- `term_trends.py` counts selected words and reports occurrences per 1,000
  tokens in each decade. Numerators and denominators use the same
  tokenizer. The output includes counts and a chart.

## Run the example

Requires Python 3.10+ and Matplotlib for the chart.

```bash
python -m pip install -r requirements.txt
python audit_corpus.py example.csv
python term_trends.py example.csv --output-dir output
```

Both scripts expect a CSV with `year` and `clean_text`. The audit also
uses optional `state`, `full_article_id`, `json_path`, and `block_id`
fields. The scripts accept years from 1840 through 1923 and use records
with at least one alphabetic token for the term-frequency calculation.
Terms are matched case-insensitively as whole tokens, without stemming.
Decade labels reflect calendar decades, with 1920–1923 as the final bin.

The chart describes word use within the input corpus. Token normalization
addresses differences in text volume, while the mix of newspapers and
records can still vary across decades. Single-word frequencies motivate
questions about framing that require reading words in context.
