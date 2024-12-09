import os
import requests


def retrieve_and_save_pfms(motifs, file_type='pfm',output_dir="pfms"):
    os.makedirs(output_dir, exist_ok=True)
    for motif in motifs:
        matrix_id = motif.get("matrix_id")
        name = motif.get("name")
        url = f"https://jaspar.genereg.net/api/v1/matrix/{matrix_id}/?format={file_type}"
        response = requests.get(url)
        if response.status_code == 200:
            # data = response.json()
            # pfm = data.get(f"{file_type}", {})
            # pfm_string = "\n".join(" ".join(map(str, row)) for row in pfm.values())
            pfm_string =  response.content.decode()
            output_file = os.path.join(output_dir, f"{matrix_id}.{file_type}")
            with open(output_file, "w") as file:
                # file.write(f">{matrix_id} {name}\n{pfm_string}")
                file.write(pfm_string)

def retrieve_and_save_versions(motifs, file_type='pfm',output_dir="pfms"):
    os.makedirs(output_dir, exist_ok=True)
    unique_base_ids = {item["base_id"] for item in motifs}
    for base_id in unique_base_ids:
        url = f"https://jaspar.elixir.no/api/v1/matrix/{base_id}/versions.{file_type}"
        response = requests.get(url)
        if response.status_code == 200:
            # data = response.json()
            # pfm = data.get(f"{file_type}", {})
            # pfm_string = "\n".join(" ".join(map(str, row)) for row in pfm.values())
            pfm_string =  response.content.decode()
            output_file = os.path.join(output_dir, f"versions.{file_type}")
            with open(output_file, "a") as file:
                # file.write(f">{matrix_id} {name}\n{pfm_string}")
                file.write(pfm_string)