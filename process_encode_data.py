#%%
import pandas as pd
import os
from multiprocessing import Pool
from modules.motif_analysis.sequence_extraction import extract_peak_sequences
from modules.motif_analysis.flanking_extraction import process_flanking_sequences_as_one_file
from modules.file_operations import log_message
#%%
def process_row(row, base_input, base_output, genome_dir, file_type):
    # Define paths for input and output
    input_file = os.path.join(
        base_output,
        row['pdbID'],
        'encode',
        row['Accession'],
        f"{row['File']}.{file_type}"
    )
    
    genome_type = row['Assembly']
    genome = os.path.join(genome_dir, f'{genome_type}.fa')

    motif_type = 'jaspar'
    
    pdbid_all_motifs = os.path.join(
        base_output,
        row['pdbID'],
        'pfms',
        f'versions.{motif_type}'
    )
    
    if not os.path.exists(pdbid_all_motifs):
        log_message('./', f'Failed to fetch Matrix_id for {row["pdbID"]}')
        return
    
    output_path = os.path.join(
        base_output,
        'analysis',
        'flanks_100bp',
        f"{row['pdbID']}"
    )
    
    peak_fasta = f"{output_path}.peak_sequences.fa"
    
    try:
        # Extract peak sequences
        extract_peak_sequences(input_file, 
                               os.path.join(base_input, genome),
                                peak_fasta,
                                overwrite='a')
    except Exception as e:
        log_message('./', f"Failed to extract PEAK sequences for: {output_path} | Error: {e}")
        return
    
    try:
        # Process motifs and flanking sequences
        process_flanking_sequences_as_one_file(peak_fasta,
                                               pdbid_all_motifs,
                                               output_path,
                                               flank_length=100,
                                               file_type=motif_type)
    except Exception as e:
        log_message('./', f"Failed to extract FLANK sequences for: {output_path} | Error: {e}")

def main():
    # Define base directories and file type
    base_input = 'input/'
    base_output = 'output/proteins/'
    file_type = 'bed'
    genome_dir = 'genome/'
        
    os.makedirs(os.path.join(base_output, 'analysis/flanks_100bp'), exist_ok=True)
    
    # Read summaries of files and motifs
    all_files_df = pd.read_csv(os.path.join(base_input, 'allFilesSummary.csv'))
    
    # Prepare arguments for parallel processing
    args = [
        (row, base_input, base_output, genome_dir, file_type)
        for _, row in all_files_df.iterrows()
    ]
    
    # Run in parallel using multiprocessing
    with Pool(processes=20) as pool:
        pool.starmap(process_row, args)

if __name__ == "__main__":
    main()

# %%
