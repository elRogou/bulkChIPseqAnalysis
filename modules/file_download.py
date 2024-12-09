import requests
import os


def download_encode_file(file_path, output_dir="downloads"):
    """
    Downloads a file from the ENCODE portal based on the provided file path.

    Args:
        file_path (str): The file path as provided in the ENCODE experiment JSON 
                         (e.g., '/files/ENCFF359JCU/@@download/ENCFF359JCU.bigBed').
        output_dir (str): The directory where the downloaded file will be saved.
                          Defaults to 'downloads'.

    Returns:
        str: The full path to the downloaded file if the download is successful.
        None: If the download fails.

    Raises:
        requests.exceptions.RequestException: If the HTTP request encounters an error.
    """
    # ENCODE base URL
    base_url = "https://www.encodeproject.org"
    
    # Construct the full URL for the file
    full_url = f"{base_url}{file_path}"
    
    # Extract the file name from the file path
    file_name = file_path.split("/")[-1]
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the local file path for saving the downloaded file
    output_file = os.path.join(output_dir, file_name)
    
    print(f"Starting download from: {full_url}")
    try:
        # Send the GET request
        response = requests.get(full_url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Write the file in chunks to avoid memory issues
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
        
        print(f"Download completed successfully. File saved to: {output_file}")
        return output_file
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {file_path}. Error: {e}")
        return None
