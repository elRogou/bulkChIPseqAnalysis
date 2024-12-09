import os
import pandas as pd
from datetime import datetime


def log_message(pdb_id_path, message):
    log_dir = os.path.join(pdb_id_path)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "process.log")

    with open(log_file, "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")
    print(message)


def create_subdirectories(base_path, subfolders, pdb_id_path):
    for subfolder in subfolders:
        path = os.path.join(base_path, subfolder)
        os.makedirs(path, exist_ok=True)
        log_message(pdb_id_path, f"Created subdirectory: {path}")


def load_encode_file(file_path, pdb_id_path):
    log_message(pdb_id_path, f"Loading ENCODE data from file: {file_path}")
    try:
        data = pd.read_csv(file_path, sep='\t')
        log_message(pdb_id_path, f"Successfully loaded ENCODE data from {file_path}")
        return data
    except Exception as e:
        log_message(pdb_id_path, f"Failed to load ENCODE data: {e}")
        raise
