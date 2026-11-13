"""Compute exploratory decade-level term frequencies and plot selected terms."""

import argparse
from collections import Counter, defaultdict
import csv
from pathlib import Path
import re

import matplotlib

from audit_corpus import read_records

matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOKEN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
TERMS = ("abortion", "eugenics", "race", "birth", "control", "court",
         "trial", "women", "children", "suicide")
PLOT_TERMS = ("abortion", "birth", "control", "court", "eugenics")


def summarize(path):
    records = Counter()
    token_totals = Counter()
    term_counts = defaultdict(Counter)
    term_set = set(TERMS)
    for year, row in read_records(path):
        tokens = TOKEN.findall((row["clean_text"] or "").casefold())
        if not tokens:
            continue
        decade = year // 10 * 10
        records[decade] += 1
        token_totals[decade] += len(tokens)
        term_counts[decade].update(token for token in tokens if token in term_set)

    if not records:
        raise ValueError("The CSV has no records with alphabetic tokens.")
    for decade in sorted(records):
        for term in TERMS:
            count = term_counts[decade][term]
            yield (decade, term, records[decade], token_totals[decade],
                   count, 1000 * count / token_totals[decade])


def write_outputs(rows, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "term_frequencies.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(("decade", "term", "records_with_tokens", "tokens",
                         "occurrences", "occurrences_per_1000_tokens"))
        writer.writerows(rows)

    figure, axis = plt.subplots(figsize=(9, 5), layout="constrained")
    for term in PLOT_TERMS:
        series = [(decade, rate) for decade, word, _, _, _, rate in rows if word == term]
        decades, rates = zip(*series)
        axis.plot(decades, rates, marker="o", label=term)
    axis.set(title="Selected terms by publication decade",
             xlabel="Decade", ylabel="Occurrences per 1,000 tokens")
    axis.legend(frameon=False)
    axis.grid(axis="y", alpha=0.25)
    figure.savefig(output_dir / "term_trends.png", dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()
    write_outputs(list(summarize(args.csv)), args.output_dir)
