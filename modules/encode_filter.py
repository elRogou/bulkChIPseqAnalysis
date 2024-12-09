import pandas as pd  # Import pandas for working with DataFrames

def filter_encode_data(df, target=None, experiment_type=None, file_type=None):
    """
    Filter ENCODE data based on specific criteria.
    
    Args:
    - df (pd.DataFrame): Pandas DataFrame containing the ENCODE data.
    - target (str): Gene or protein target (e.g., TP53).
    - experiment_type (str): Type of experiment (e.g., ChIP-seq).
    - file_type (str): Type of file (e.g., bigWig, bed).
    
    Returns:
    - pd.DataFrame: A filtered DataFrame.
    """
    filtered_df = df

    # Filter by target
    if target:
        filtered_df = filtered_df[filtered_df["Target of assay"].str.contains(target, na=False, case=False)]

    # Filter by experiment type
    if experiment_type:
        filtered_df = filtered_df[filtered_df["Assay name"].str.contains(experiment_type, na=False, case=False)]

    # # Filter by file type
    if file_type:
        filtered_df = filtered_df[filtered_df['Files'].str.contains(file_type, na=False, case=False)]

    return filtered_df

def verify_file(file_info,file_type='bed'):
    """
    Verifying the file is released and default.
    
    Args:
    - file_info (dict): file info from json data of experiment.
    - file_type (str): Type of file (e.g., bigWig, bed).
    
    Returns:
    - pd.DataFrame: A filtered DataFrame.
    """
    if file_info.get("file_format") == file_type and\
        "href" in file_info and\
        "preferred_default" in file_info and\
        file_info['analyses'][0]["status"] == 'released':

        return True
