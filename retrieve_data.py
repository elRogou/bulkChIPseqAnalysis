#%% 
from modules.file_operations import log_message, create_subdirectories, load_encode_file
from modules.api_operations import get_uniprot_id, get_gene_name, fetch_encode_experiment, fetch_motifs_by_name
from modules.motif_operations import retrieve_and_save_pfms
from modules.encode_filter import filter_encode_data, verify_file
from modules.file_download import download_encode_file
import pandas as pd
import shutil


def main():
    # pdb_ids = pd.read_csv("input/pdb_ids.txt", header=None)[0].tolist()
    pdb_ids = pd.read_csv('input/filtered_sorted_pdbids.csv')
    # pdb_ids = ['1g9y']
    encode_file = "input/encode/experiment_report_2024_12_3_8h_4m.tsv"
    subfolders = ["encode", "pfms"]

    proteins_summary_df = pd.DataFrame(columns=["pdbID", "UniProt", "Gene name"])
    encode_files_summary  = pd.DataFrame(columns=["pdbID", "Accession","File",'Assembly'])
    encode_df = load_encode_file(encode_file, './')

    count = 0
    for pdb_id in pdb_ids['pdbid']:
        pdb_id = pdb_id.strip()
        pdb_id_path = 'output/proteins/'+pdb_id
        create_subdirectories(pdb_id_path, subfolders, pdb_id_path)

        uniprot_id = get_uniprot_id(pdb_id)
        if not uniprot_id:
            log_message(pdb_id_path, "UniProt ID not found.")
            shutil.rmtree(pdb_id_path)
            continue
        else:
            log_message(pdb_id_path, f"Identified UniProt ID: {uniprot_id}.")

        gene_name = get_gene_name(uniprot_id)
        if (not gene_name or len(gene_name)<2) or (gene_name in proteins_summary_df["Gene name"].values):
            log_message(pdb_id_path, "Gene name not found or exists.")
            shutil.rmtree(pdb_id_path)
            continue
        else:
            log_message(pdb_id_path, f"Identified gene name {gene_name}.")

        motifs = fetch_motifs_by_name(gene_name)
        if not motifs:
            log_message(pdb_id_path, f"No Motifs found for {gene_name}.")
            shutil.rmtree(pdb_id_path)

        retrieve_and_save_pfms(motifs, output_dir=f"{pdb_id_path}/pfms")


        filtered_df = filter_encode_data(encode_df, target=gene_name, experiment_type="ChIP-seq")
        if filtered_df.empty:
            log_message(pdb_id_path, f"No ENCODE data found for gene {gene_name}.")
            shutil.rmtree(pdb_id_path)
            continue

        log_message(pdb_id_path, f"Filtered ENCODE data for {gene_name} contains {len(filtered_df)} rows.")

        proteins_summary_df.loc[count] = [pdb_id,uniprot_id,gene_name]
        count+=1

        # Step 7: Process each accession in filtered ENCODE data
        for accession in filtered_df["Accession"]:
            experiment_dir = f"{pdb_id_path}/encode/{accession}"
            create_subdirectories(pdb_id_path, [f"encode/{accession}"], pdb_id_path)

            # Fetch experiment data and save JSON
            experiment_data = fetch_encode_experiment(accession, output_file=f"{experiment_dir}/{accession}.json")
            if experiment_data:
                log_message(pdb_id_path, f"Experiment data for accession {accession} saved to {experiment_dir}/{accession}.json.")
                
                # Download associated files if available
                for file_info in experiment_data.get("files", []):
                    if verify_file(file_info):
                        file_path = file_info["href"]
                        downloaded_file = download_encode_file(file_path, output_dir=experiment_dir)
                        if downloaded_file:
                            log_message(pdb_id_path, f"File downloaded for accession {accession}: {downloaded_file}")
                            
                            encode_files_summary.loc[count] = {
                                    'pdbID': pdb_id,
                                    'Accession': accession,
                                    'File': file_info['accession'],
                                    'Assembly': file_info['assembly']
                                    }
                            count+=1
                        else:
                            log_message(pdb_id_path, f"Failed to download file for accession {accession}: {file_path}")
            else:
                log_message(pdb_id_path, f"No experiment data available for accession {accession}.")
    encode_files_summary.to_csv('input/allFilesSummary.csv', index=False)
    proteins_summary_df.to_csv('input/proteinsSummary.csv', index=False)

if __name__ == "__main__":
    main()

# %%
