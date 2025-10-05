<div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.6; color: #24292e; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">

<h1 style="color: #0366d6; border-bottom: 2px solid #eaecef; padding-bottom: 6px;">Data Analysis of Signal Peptides</h1>

<p>This repository contains the work carried out for the Data Analysis. The goal was to analyze datasets of proteins with and without signal peptides, perform descriptive statistical analyses, and visualize key features such as sequence lengths, amino acid compositions, taxonomic distribution, and cleavage site motifs.</p>

<h2 style="color: #22863a; border-bottom: 1px solid #eaecef;">Workflow and Steps</h2>

<h3 style="color: #6f42c1;">1. Dataset Retrieval</h3>
<p>We retrieved the datasets from <strong>UniProtKB/SwissProt</strong>, selecting proteins annotated with a signal peptide (positive set) and proteins without signal peptides (negative set). The data was downloaded in TSV format and included metadata such as:</p>
<ul style="margin-left: 20px;">
  <li>Accession</li>
  <li>Organism</li>
  <li>Kingdom</li>
  <li>Sequence length</li>
  <li>Signal peptide cleavage site</li>
</ul>
<p>This gave us a clear starting point with both positive and negative examples for further analysis.</p>



<h3 style="color: #6f42c1;">2. Data Preprocessing</h3>
<p>The raw dataset was curated to ensure quality:</p>
<ul style="margin-left: 20px;">
  <li>Removed redundant entries and incomplete sequences.</li>
  <li>Verified that both positive and negative datasets were properly balanced.</li>
  <li>Added a <code style="background-color: #f6f8fa; padding: 2px 5px; border-radius: 4px;">fold</code> column to split the data into 5 partitions for cross-validation.</li>
</ul>
<p>After preprocessing, the dataset was ready for statistical analysis.</p>



<h3 style="color: #6f42c1;">3. Protein Length Distribution</h3>
<p>The first descriptive analysis compared the lengths of proteins containing signal peptides against those without. A histogram/density plot was generated to visualize the distribution.</p>
<p>The analysis showed that signal peptide-containing proteins were, on average, slightly longer than proteins without SPs. This confirmed the expectation that secretory proteins tend to have longer sequences.</p>

<img src="./1.protein length/test_protein_lengths.png" alt="Protein length distribution plot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
<img src="./1.protein length/training_protein_lengths.png" alt="Protein length distribution plot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">

<h3 style="color: #6f42c1;">4. Signal Peptide Length Distribution</h3>
<p>We then focused on the signal peptides themselves:</p>
<ul style="margin-left: 20px;">
  <li>Extracted SP regions from the positive dataset.</li>
  <li>Produced a histogram of SP lengths.</li>
</ul>
<p>The distribution centered around <strong>~20–25 amino acids</strong>, with most SPs falling within this narrow range. This is consistent with known biology, as signal peptides are typically short hydrophobic sequences that guide protein secretion.</p>

<img src="./2.SP length/test_sp_lengths.png" alt="Signal peptide length distribution plot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
<img src="./2.SP length/training_sp_lengths.png" alt="Signal peptide length distribution plot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">

<h3 style="color: #6f42c1;">5. Amino Acid Composition Analysis</h3>
<p>To understand compositional biases, we compared amino acid frequencies in SPs against the background amino acid distribution of SwissProt:</p>
<ul style="margin-left: 20px;">
  <li>Calculated amino acid usage across all SPs.</li>
  <li>Downloaded SwissProt composition statistics from Expasy.</li>
  <li>Created a combined barplot for comparison.</li>
</ul>
<p><strong>Findings:</strong></p>
<ul style="margin-left: 20px;">
  <li>SPs are enriched in hydrophobic residues such as <strong>L, I, V, A, F, and M</strong>.</li>
  <li>Polar and charged residues were under-represented.</li>
</ul>
<p>This matched the expected hydrophobic character of SPs.</p>

<img src="./3.AA/test_aa_comp.png" alt="Amino acid composition comparison plot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
<img src="./3.AA/training_aa_comp.png" alt="Amino acid composition comparison plot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">

<h3 style="color: #6f42c1;">6. Taxonomic Classification</h3>
<p>We analyzed the dataset by <strong>Kingdom</strong> and <strong>Species</strong>:</p>
<ul style="margin-left: 20px;">
  <li>Grouped proteins by taxonomy and plotted their frequencies.</li>
</ul>
<p>At the kingdom level, SP-containing proteins appeared across <em>Bacteria</em>, <em>Eukaryota</em>, and <em>Archaea</em>, with <strong>Eukaryotes</strong> dominating the dataset.</p>
<p>At the species level, the dataset showed a broad distribution, confirming it was not biased toward a single organism.</p>
<p>We used barplots for clarity.</p>

<img src="./4.Clasification/test_kingdom.png" alt="Taxonomic distribution barplot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
<img src="./4.Clasification/training_kingdom.png" alt="Taxonomic distribution barplot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
<img src="./4.Clasification/test_organism.png" alt="Taxonomic distribution barplot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
<img src="./4.Clasification/training_organism.png" alt="Taxonomic distribution barplot" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">

<h3 style="color: #6f42c1;">7. Cleavage Site Sequence Logos</h3>
<p>Finally, we examined the signal peptide cleavage sites:</p>
<ul style="margin-left: 20px;">
  <li>Extracted regions from <code style="background-color: #f6f8fa; padding: 2px 5px; border-radius: 4px;">-13</code> to <code style="background-color: #f6f8fa; padding: 2px 5px; border-radius: 4px;">+2</code> around the cleavage position.</li>
  <li>Aligned these subsequences.</li>
  <li>Submitted the alignment to <a href="https://weblogo.berkeley.edu" target="_blank" style="color: #0366d6; text-decoration: none;">WebLogo</a> to generate a sequence logo.</li>
</ul>
<p>The resulting logo highlighted:</p>
<ul style="margin-left: 20px;">
  <li>Strong conservation of <strong>Alanine (A)</strong> at position <strong>-1</strong>.</li>
</ul>
<p>This observation matches <strong>von Heijne’s rules</strong>, which describe conserved residues around cleavage sites.</p>

<img src="./5.cleavage site/weblogo.png" alt="Signal peptide cleavage site logo" width="600" style="display:block; margin: 15px auto; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">

</div>
