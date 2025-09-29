# requirements: biopython, pandas
# pip install biopython pandas

from pathlib import Path
import re
import pandas as pd
from Bio import SeqIO

# ---- Paths ----
FASTA_IN = Path("cluster-results1_rep_seq.fasta")
TSV_IN = Path("training_with_folds.tsv")
FASTA_OUT = Path("selected_sequences_window_-13_to_+2.fasta")
SKIPPED_OUT = Path("skipped_rows_missing_seq_or_cleavage.txt")

# ---- Helpers ----
def extract_uniprot_accession(header: str) -> str | None:
    """
    Extract a UniProt accession (optionally with isoform suffix -N) from a FASTA header.
    Supports headers like:
      >sp|P12345|..., >tr|A0A123ABC4|..., >UniProtKB:P12345 ...
      >P12345 some desc
    """
    if header.startswith(("sp|", "tr|")):
        parts = header.split("|", 2)
        if len(parts) >= 2:
            return parts[1].strip()
    m = re.search(r"\bUniProtKB:([A-Z0-9]+(?:-\d+)?)\b", header)
    if m:
        return m.group(1)
    tok = header.split(None, 1)[0]
    cand = tok.split("|")[-1]
    if re.fullmatch(r"(?:[A-Z0-9]{6}|[A-Z0-9]{10})(?:-\d+)?", cand):
        return cand
    m2 = re.search(r"\b((?:[A-Z0-9]{6}|[A-Z0-9]{10})(?:-\d+)?)\b", header)
    return m2.group(1) if m2 else None

def build_acc_to_seq(fasta_path: Path) -> dict[str, str]:
    """Map accession -> sequence (also index by base accession without isoform)."""
    acc_to_seq: dict[str, str] = {}
    with open(fasta_path, "r") as fh:
        for rec in SeqIO.parse(fh, "fasta"):
            header = rec.description
            acc = extract_uniprot_accession(header)
            if not acc:
                continue
            base = acc.split("-")[0]
            seq = str(rec.seq).upper().replace(" ", "").replace("\n", "")
            acc_to_seq.setdefault(acc, seq)
            acc_to_seq.setdefault(base, seq)
    return acc_to_seq

# ---- Main ----
def main():
    df = pd.read_csv(TSV_IN, sep="\t", dtype=str)
    for col in ("Accession", "SP cleavage"):
        if col not in df.columns:
            raise ValueError(f"Missing required column '{col}' in {TSV_IN}")

    accessions = df["Accession"].astype(str).str.strip()
    cleavage_raw = df["SP cleavage"]

    acc_to_seq = build_acc_to_seq(FASTA_IN)

    written = 0
    skipped = []

    with open(FASTA_OUT, "w") as out_f:
        for i, (acc, cleav) in enumerate(zip(accessions, cleavage_raw)):
            if not acc or pd.isna(cleav):
                skipped.append((i, acc, cleav, "missing accession or cleavage"))
                continue

            # Parse cleavage site (often '22.0' in TSV) as 1-based position of the cleavage residue.
            try:
                P1 = int(float(cleav))
            except Exception:
                skipped.append((i, acc, cleav, "invalid cleavage value"))
                continue

            # Retrieve sequence by exact accession, then base accession (without isoform)
            seq = acc_to_seq.get(acc) or acc_to_seq.get(acc.split("-")[0])
            if not seq:
                skipped.append((i, acc, cleav, "sequence not found in FASTA"))
                continue

            # j is 0-based index of the cleavage residue
            j = P1

            # Preferred window [j-13 : j+2] inclusive  -> Python slice [j-13 : j+3]
            start0 = j - 13
            end0_exclusive = j + 2

            if start0 < 0 or end0_exclusive > len(seq):
                skipped.append(
                    (i, acc, cleav,
                     f"window out of bounds (len={len(seq)}, start0={start0}, end0={end0_exclusive})")
                )
                continue

            window = seq[start0:end0_exclusive]  # length should be 16

            out_f.write(f">{acc}|cleavage={P1}|window=-13..+2\n")
            for k in range(0, len(window), 60):
                out_f.write(window[k:k+60] + "\n")
            written += 1

    with open(SKIPPED_OUT, "w") as fh:
        for i, acc, cleav, reason in skipped:
            fh.write(f"row={i}\tAccession={acc}\tSP_cleavage={cleav}\treason={reason}\n")

    print(f"Written windows: {written}")
    print(f"Skipped rows: {len(skipped)}")
    print(f"Output FASTA: {FASTA_OUT}")
    print(f"Diagnostics:  {SKIPPED_OUT}")

if __name__ == "__main__":
    main()
