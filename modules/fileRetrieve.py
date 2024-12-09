import requests
import pandas as pd
import json
import os

def get_uniprot_id(pdb_id):
    """
    Retrieve the UniProt ID for a given PDB ID using the PDBe API.
    """
    url = f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return list(data[pdb_id]["UniProt"].keys())[0]
    else:
        print(f"Failed to retrieve data for PDB ID: {pdb_id} (Status code: {response.status_code})")
        return None


def get_gene_name(uniprot_id):
    """
    Retrieve the gene name for a given UniProt ID using the UniProt API.
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Extract the gene name
        genes = data.get("genes", [])
        if genes:
            return genes[0].get("geneName", {}).get("value")
        else:
            print(f"No gene information found for UniProt ID: {uniprot_id}")
            return None
    else:
        print(f"Failed to retrieve data for UniProt ID: {uniprot_id} (Status code: {response.status_code})")
        return None

def load_encode_file(file_path):
    """
    Load an ENCODE TSV file into a Pandas DataFrame.
    
    Args:
    - file_path: Path to the ENCODE TSV file.
    
    Returns:
    - A Pandas DataFrame containing the data.
    """
    try:
        # Read the TSV file
        df = pd.read_csv(file_path, sep="\t", engine="python")
        print(f"File loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def filter_encode_data(df, target=None, experiment_type=None, file_type=None):
    """
    Filter ENCODE data based on specific criteria.
    
    Args:
    - df: Pandas DataFrame containing the ENCODE data.
    - target: Gene or protein target (e.g., TP53).
    - experiment_type: Type of experiment (e.g., ChIP-seq).
    - file_type: Type of file (e.g., bigWig, bed).
    
    Returns:
    - A filtered DataFrame.
    """
    filtered_df = df

    # Filter by target
    if target:
        filtered_df = filtered_df[filtered_df["Target of assay"].str.contains(target, na=False, case=False)]

    print(f"Filtered data contains {len(filtered_df)} rows.")
    return filtered_df

def fetch_motifs_by_name(name):
    """
    Fetch motifs from JASPAR API by motif name or transcription factor name.

    Parameters:
        name (str): The name to search (e.g., gene name, transcription factor).

    Returns:
        list: A list of motif metadata (e.g., matrix IDs and details).
    """
    url = f"https://jaspar.genereg.net/api/v1/matrix/?name={name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        api_response = response.json()
        motifs = api_response.get('results', [])  # Extract 'results' key
        print(f"Found {len(motifs)} motifs for name '{name}'.")
        return motifs
    else:
        print(f"Error fetching motifs: {response.status_code}")
        return []

def retrieve_and_save_pfms(motifs, output_dir="pfms"):
    """
    Retrieve PFMs for each motif and save them to separate files.

    Parameters:
        motifs (list): List of motif metadata (e.g., from fetch_motifs_by_name).
        output_dir (str): Directory to save the PFM files.

    Returns:
        None
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for motif in motifs:
        matrix_id = motif.get('matrix_id')
        name = motif.get('name')

        # Construct PFM URL
        url = f"https://jaspar.genereg.net/api/v1/matrix/{matrix_id}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Save PFM to a file
            data = response.json()
        # Extract the gene name
            pfm = data.get("pfm", {})
            pfm_string = "\n".join(" ".join(map(str, row)) for row in pfm.values())
            
            # Save to a file
            output_file = os.path.join(output_dir, f"{matrix_id}_{name}_pfm.txt")
            with open(output_file, "w") as file:
                file.write(f">Matrix ID: {matrix_id} ({name})\n")
                file.write(pfm_string)
            print(f"PFM saved for {name} (Matrix ID: {matrix_id}) at {output_file}.")
        else:
            print(f"Error fetching PFM for {matrix_id}: {response.status_code}")