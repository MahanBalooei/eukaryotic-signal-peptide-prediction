# LB2_project_Group_7
## Project Overview: Eukaryotic Signal Peptide Dataset Collection
This project focuses on creating a high-quality, balanced dataset for signal peptide (SP) prediction in eukaryotic proteins. By optimizing UniProt data, we collect preliminary positive and negative examples based on strict experimental evidence criteria. The resulting datasets are formatted for downstream machine learning applications in bioinformatics.

# Dataset Collection Workflow
Initial datasets are programmatically retrieved from UniProt in JSON format and applying the specified filters during query construction.
Raw JSON data is imported into Google Colab for comprehensive parsing, validation, additional filtering, and quality control to ensure compliance with all criteria. The complete data processing workflow, including filtering logic, quality checks, and statistical analysis, is documented in Jupyter notebook (.ipynb) format for full transparency and reproducibility. Post-processed data is exported in standardized TSV and FASTA formats, ready for model training and analysis.

## Positive Data (Sequences with Signal Peptides)
We retrieve eukaryotic proteins experimentally confirmed to possess signal peptides, applying the following filters:
- No fragments: Full-length proteins only.
- Eukaryotic origin: Limited to eukaryotic taxonomy.
- Length filter: Sequences ≥ 40 residues.
- Reviewed status: UniProt-reviewed (Swiss-Prot) entries only.
- SP evidence: Experimental confirmation of SP presence.
- SP length: Mature SP ≥ 14 residues.
- Protein existence: Evidence at the protein level (PE1).
- Cleavage site: Confirmed existence.

## Negative Data (Sequences without Signal Peptides)
We select eukaryotic proteins experimentally verified to lack SPs and localize to non-secretory compartments, with these filters:
- No fragments: Full-length proteins only.
- Reviewed status: UniProt-reviewed (Swiss-Prot) entries only.
- Protein existence: Evidence at the protein level (PE1).
- Eukaryotic origin: Limited to eukaryotic taxonomy.
- Length filter: Sequences ≥ 40 residues.
- No SP evidence: Explicitly filtered for absence of any SP (regardless of evidence level).
- Localization: Experimentally verified to cytosol, nucleus, mitochondrion, plastid, peroxisome, or cell membrane.

# Data Storage and Formatting
## TSV format:
- Positive: Tab-separated values with columns: Accession, Organism, Kingdom, Sequence length, SP cleavage
- Negative: Tab-separated values with columns: Accession, Organism, Kingdom, Sequence length, N-term, transmembrane
- ## FASTA format:
Standard sequence headers including UniProt ID and metadata.




## Dataset Statistics
After UniProt retrieval and Google Colab processing, the final filtered dataset statistics are:

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Total</th>
      <th>Filtered</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Positive</td>
      <td>2949</td>
      <td>2932</td>
    </tr>
    <tr>
      <td>Negative</td>
      <td>20615</td>
      <td>20615</td>
    </tr>
  </tbody>
</table>
