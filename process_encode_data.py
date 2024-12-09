# Retrieving flanks for proteins in df:
# 1. fetch list of bed files
# 2. get fasta of peaks using genome
# 3. fetch pfms
# 4. for each pfm fetch flanks, right and left
# the data will be the following:
# for every protein, for every ChIPseq experinment, for every bed file in experiment
# for every pfm, there will be two fa files - left and right.
# Is it correct to join them?
# The filename cxan be the following:
# {pdb_id}.{experiment}.{bed_filename}.{pfm}.LF.fa
# {pdb_id}.{experiment}.{bed_filename}.{pfm}.RF.fa
# in a single analysis folders in output folder.

# When running main:
# create output/analysis
# load the data with pdb_ids
# fetch list of files, clever, no glob, maybe should be
# saved with pdb_ids when running encode retrieval?

# %%
import pandas as pd
import os
from modules.motif_analysis.sequence_extraction import extract_peak_sequences
from modules.motif_analysis.flanking_extraction import process_flanking_sequences
from modules.file_operations import log_message

def main():
    # Define base directories and file type
    base_input = 'input/'
    base_output = 'output/proteins/'
    file_type = 'bed'

    genome_dir = 'genome/'
        
    os.makedirs(os.path.join(base_output,'analysis/flanks_100bp'), exist_ok=True)

    # Read summaries of files and motifs
    all_files_df = pd.read_csv(os.path.join(base_input, 'allFilesSummary.csv'))
    all_motifs_df = pd.read_csv(os.path.join(base_input, 'allMotifsSummary.csv'))
    
    # Process each file and corresponding motifs
    for i, row in all_files_df.iterrows():
        input_file = os.path.join(
            base_output,
            row['pdbID'],
            'encode',
            row['Accession'],
            f"{row['File']}.{file_type}"
        )
        
        genome_type = row['Assembly']

        genome = os.path.join(genome_dir,f'{genome_type}.fa')
        
        pdbid_all_motifs = all_motifs_df[all_motifs_df['pdbID'] == row['pdbID']]['Matrix_id']

        if pdbid_all_motifs.empty:
            log_message('./',f'Failed to fetch Matrix_id for {row["pdbID"]}')
            continue

        for matrix_id in pdbid_all_motifs:
            matrix_id_file = os.path.join(
                base_output,
                row['pdbID'],
                'pfms',
                f"{matrix_id}.pfm"
            )
            
            output_path = os.path.join(
                base_output,
                'analysis',
                f"{row['pdbID']}.{row['Accession']}.{row['File']}"
            )
            
            peak_fasta = f"{output_path}.peak_sequences.fa"

            try:
                # Extract peak sequences
                extract_peak_sequences(input_file, os.path.join(base_input, genome), peak_fasta)
            except:
                log_message('./', f"Failed to exctract PEAK sequences for: {output_path}")
            
            try:
                # Process motifs and flanking sequences
                process_flanking_sequences(peak_fasta, matrix_id_file, output_path)
            except:
                log_message('./', f"Failed to exctract FLANK sequences for: {output_path}")

        # break

if __name__ == "__main__":
    main()

# %%