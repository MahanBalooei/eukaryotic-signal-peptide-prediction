<div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.6; color: #24292e; background-color: #ffffff; padding: 25px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">

<h1 style="color: #0366d6; border-bottom: 2px solid #eaecef; padding-bottom: 6px;">Data Analysis of Signal Peptides</h1>

<h2 style="color: #22863a;">Introduction</h2>
<p>Signal peptides (SPs) are short N-terminal sequences that direct newly synthesized proteins to the secretory pathway. They act like “postal codes,” guiding proteins toward the endoplasmic reticulum (in eukaryotes) or the plasma membrane (in prokaryotes). Once the protein reaches its destination, the signal peptide is typically cleaved off by signal peptidases.</p>

<p>Understanding signal peptides is fundamental in bioinformatics because they determine whether a protein is secreted or membrane-bound. In this project, we focus on <strong>analyzing datasets of proteins with and without signal peptides</strong> to identify features that distinguish them. These descriptive analyses form the foundation for later predictive modeling, such as implementing <strong>von Heijne’s rules</strong> or training an <strong>SVM classifier</strong>.</p>

<hr style="border: 1px solid #eaecef; margin: 25px 0;">

<h2 style="color: #22863a;">Workflow Overview</h2>
<p>The data analysis followed the LB2 Project plan and aimed to explore dataset quality and biological patterns before applying machine learning. The workflow included:</p>
<ul style="margin-left: 20px;">
  <li><strong>Dataset retrieval</strong> from UniProtKB/SwissProt (positive: with SP, negative: without SP).</li>
  <li><strong>Data preprocessing</strong> for cleaning, balancing, and preparing 5-fold cross-validation splits.</li>
  <li><strong>Descriptive analyses</strong> to study sequence lengths, amino acid composition, taxonomy, and motifs.</li>
  <li><strong>Visualization</strong> using histograms, barplots, and sequence logos to interpret patterns.</li>
</ul>

<p>Each step was performed using <strong>Pandas</strong>, <strong>Matplotlib/Seaborn</strong>, and <strong>WebLogo</strong> for motif visualization.</p>

<hr style="border: 1px solid #eaecef; margin: 25px 0;">

<h3 style="color: #6f42c1;">1. Protein Length Distribution</h3>
<p><strong>Goal:</strong> Compare protein lengths between sequences containing signal peptides (SP+) and those without (SP−).</p>

<p><strong>Method:</strong> The total sequence lengths of both positive and negative proteins were extracted and visualized using histograms and density plots for both <em>training</em> and <em>test</em> sets. These plots reveal how protein size varies across the two groups.</p>

<div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
  <img src="./1.protein length/test_protein_lengths.png" alt="Protein length - Test" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
  <img src="./1.protein length/training_protein_lengths.png" alt="Protein length - Train" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
</div>

<p><strong>Interpretation:</strong> The histograms show that proteins containing signal peptides are, on average, slightly longer than those without. This makes biological sense: secretory proteins often have longer signal regions and extracellular domains. Verifying this difference also ensures that the dataset reflects realistic biological diversity, not artificial bias.</p>

<hr style="border: 1px solid #eaecef; margin: 25px 0;">

<h3 style="color: #6f42c1;">2. Signal Peptide Length Distribution</h3>
<p><strong>Goal:</strong> Explore the variability in the length of signal peptides themselves.</p>

<p><strong>Method:</strong> From the positive dataset, only the annotated SP segments were extracted. Their lengths were measured and visualized as histograms for both the training and test sets. This helps determine whether SPs follow expected biological length ranges.</p>

<div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
  <img src="./2.SP length/test_sp_lengths.png" alt="SP length - Test" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
  <img src="./2.SP length/training_sp_lengths.png" alt="SP length - Train" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
</div>

<p><strong>Interpretation:</strong> Most signal peptides fall within 20–25 amino acids, consistent with their known structural function: forming a short hydrophobic stretch that fits into the translocon channel during protein export. This also validates that the dataset annotations are biologically correct and not random.</p>

<hr style="border: 1px solid #eaecef; margin: 25px 0;">

<h3 style="color: #6f42c1;">3. Amino Acid Composition</h3>
<p><strong>Goal:</strong> Identify compositional biases of signal peptides compared to average SwissProt proteins.</p>

<p><strong>Method:</strong> Amino acid frequencies were computed from all SP sequences and compared with reference frequencies from <a href="https://web.expasy.org/docs/relnotes/relstat.html" target="_blank" style="color: #0366d6;">SwissProt statistics</a>. Barplots were generated for both datasets to visualize enrichment or depletion of specific residues.</p>

<div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
  <img src="./3.AA/test_aa_comp.png" alt="AA composition - Test" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
  <img src="./3.AA/training_aa_comp.png" alt="AA composition - Train" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
</div>

<p><strong>Interpretation:</strong> Signal peptides are highly enriched in <strong>hydrophobic residues</strong> (Leucine, Isoleucine, Valine, Alanine, Phenylalanine, Methionine) and depleted in charged or polar residues. This reflects their role in embedding into lipid bilayers during targeting. The compositional profile therefore serves as a strong discriminative feature for SP prediction algorithms.</p>

<hr style="border: 1px solid #eaecef; margin: 25px 0;">

<h3 style="color: #6f42c1;">4. Taxonomic Classification</h3>
<p><strong>Goal:</strong> Assess whether the dataset is taxonomically balanced and biologically representative.</p>

<p><strong>Method:</strong> Protein entries were grouped by <em>Kingdom</em> and <em>Organism</em>. The counts were visualized with barplots for both the training and test datasets. This ensures the model will generalize across diverse biological taxa rather than overfitting to one species.</p>

<div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
  <img src="./4.Clasification/test_kingdom.png" alt="Taxonomy - Test Kingdom" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
  <img src="./4.Clasification/training_kingdom.png" alt="Taxonomy - Train Kingdom" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
  <img src="./4.Clasification/test_organism.png" alt="Taxonomy - Test Organism" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
  <img src="./4.Clasification/training_organism.png" alt="Taxonomy - Train Organism" width="48%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
</div>

<p><strong>Interpretation:</strong> The barplots show that SP-containing proteins appear across all three domains of life—<em>Bacteria, Archaea,</em> and <em>Eukaryota</em>—with Eukaryotic sequences dominating the dataset. This confirms that signal peptides are a universal mechanism, but the model must account for taxonomic composition during training to avoid bias.</p>

<hr style="border: 1px solid #eaecef; margin: 25px 0;">

<h3 style="color: #6f42c1;">5. Cleavage Site Sequence Logos</h3>
<p><strong>Goal:</strong> Visualize conserved residues surrounding signal peptide cleavage sites.</p>

<p><strong>Method:</strong> A window from <code>-13</code> to <code>+2</code> relative to the cleavage position was extracted from each positive sequence and aligned. These regions were submitted to <a href="https://weblogo.berkeley.edu" target="_blank" style="color: #0366d6;">WebLogo</a> to generate a sequence logo summarizing residue conservation patterns.</p>

<div style="display: flex; justify-content: center;">
  <img src="./5.cleavage site/weblogo.png" alt="Cleavage site sequence logo" width="70%" style="border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
</div>

<p><strong>Interpretation:</strong> The sequence logo shows a strong conservation of <strong>Alanine (A)</strong> at position <strong>-1</strong> and small residues near the cleavage site, supporting <strong>von Heijne’s rules</strong> of signal peptide cleavage. This motif-level analysis bridges sequence statistics with functional biology, confirming the reliability of our dataset annotations.</p>

<hr style="border: 1px solid #eaecef; margin: 25px 0;">

<h3 style="color: #6f42c1;">Conclusion</h3>
<p>This analysis provided a comprehensive understanding of the dataset used for signal peptide prediction. By combining descriptive statistics and biological interpretation, we confirmed that the dataset is balanced, biologically coherent, and ready for downstream feature extraction and machine learning steps. The observed properties—hydrophobic composition, specific length ranges, and conserved cleavage motifs—align perfectly with the known biology of signal peptides and validate the preprocessing process.</p>

</div>
