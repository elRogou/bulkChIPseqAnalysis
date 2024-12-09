import requests
import json


def get_uniprot_id(pdb_id):
    """
    Retrieve the UniProt ID for a given PDB ID using the PDBe API.

    Args:
        pdb_id (str): The PDB ID for which the UniProt ID needs to be retrieved.

    Returns:
        str: The UniProt ID if found, or None if not found or an error occurs.
    """
    url = f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if pdb_id in data and "UniProt" in data[pdb_id]:
            return list(data[pdb_id]["UniProt"].keys())[0]
        else:
            print(f"No UniProt ID mapping found for PDB ID: {pdb_id}")
            return None
    else:
        print(f"Failed to retrieve data for PDB ID: {pdb_id}. Status code: {response.status_code}")
        return None


def get_gene_name(uniprot_id):
    """
    Retrieve the gene name for a given UniProt ID using the UniProt API.

    Args:
        uniprot_id (str): The UniProt ID for which the gene name needs to be retrieved.

    Returns:
        str: The gene name if found, or None if not found or an error occurs.
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        genes = data.get("genes", [])
        if genes:
            return genes[0].get("geneName", {}).get("value", None)
        else:
            print(f"No gene information found for UniProt ID: {uniprot_id}")
            return None
    else:
        print(f"Failed to retrieve data for UniProt ID: {uniprot_id}. Status code: {response.status_code}")
        return None


def fetch_motifs_by_name(name):
    """
    Fetch motifs from the JASPAR API by name.

    Args:
        name (str): The name to search for (e.g., a gene or transcription factor name).

    Returns:
        list: A list of motifs (as dictionaries) retrieved from the JASPAR API, or an empty list if none are found.
    """
    url = f"https://jaspar.genereg.net/api/v1/matrix/?name={name}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get("results", [])
        print(f"Found {len(results)} motifs for name {name}.")
        return results
    else:
        print(f"Error fetching motifs for '{name}'. Status code: {response.status_code}")
        return []


def fetch_encode_experiment(accession, output_file=None):
    """
    Fetch ENCODE experiment JSON data by accession ID.

    Args:
        accession (str): The ENCODE experiment accession ID (e.g., 'ENCSR000AAX').
        output_file (str, optional): The file path to save the JSON data. Defaults to None.

    Returns:
        dict: The JSON response from the ENCODE API if successful, or None if an error occurs.
    """
    url = f"https://www.encodeproject.org/experiments/{accession}/?format=json"
    response = requests.get(url, headers={"Accept": "application/json"})

    if response.status_code == 200:
        data = response.json()
        if output_file:
            with open(output_file, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Experiment data saved to {output_file}.")
        return data
    else:
        print(f"Error fetching experiment data for accession {accession}. Status code: {response.status_code}")
        return None
