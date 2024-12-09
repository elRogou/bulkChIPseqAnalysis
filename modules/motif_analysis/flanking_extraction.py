from Bio import SeqIO, motifs
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
from Bio.motifs import motifs


import os

def process_flanking_sequences(fasta_file, pfm_file, output_path, flank_length=10):
    """
    Identifies motifs in peak sequences and extracts left and right flanking sequences.

    Args:
        fasta_file (str): Path to the FASTA file containing peak sequences.
        pfm_file (str): Path to the PFM (Position Frequency Matrix) file.
        output_path (str): Base path to save the left and right flanking sequences.
        flank_length (int): Length of the flanking sequence to extract.
    """
    with open(pfm_file) as motif_file:
        all_motifs = list(motifs.parse(motif_file, "jaspar"))
    
    for motif in all_motifs:
        left_output_fasta = f"{output_path}.{motif.matrix_id}.LF.fa"
        right_output_fasta = f"{output_path}.{motif.matrix_id}.RF.fa"
        
        left_records, right_records = [], []
        
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(record.seq)
            
            for pos, _ in motif.pssm.search(sequence, threshold=0.9):  # Adjust threshold as needed
                start, end = pos, pos + len(motif)
                
                left_flank = sequence[start - flank_length:start]
                right_flank = sequence[end:end + flank_length]
                
                if len(left_flank) < flank_length or len(right_flank) < flank_length:
                    continue
                
                left_records.append(SeqRecord(
                    Seq(left_flank),
                    id=f"{record.id}_{start}_{end}_left",
                    description=f"Left flank from {start - flank_length} to {start}"
                ))
                
                right_records.append(SeqRecord(
                    Seq(right_flank),
                    id=f"{record.id}_{start}_{end}_right",
                    description=f"Right flank from {end} to {end + flank_length}"
                ))
        
        SeqIO.write(left_records, left_output_fasta, "fasta")
        SeqIO.write(right_records, right_output_fasta, "fasta")
        print(f"Left flanking sequences saved to {left_output_fasta}")
        print(f"Right flanking sequences saved to {right_output_fasta}")

def process_flanking_sequences_as_one_file(fasta_file, pfm_file, output_file, flank_length=10):
    """
    Identifies motifs in peak sequences and directly writes left and right flanking sequences to an output file.
    Appends to an existing file if it already exists.

    Args:
        fasta_file (str): Path to the FASTA file containing peak sequences.
        pfm_file (str): Path to the PFM (Position Frequency Matrix) file.
        output_file (str): Path to the output file where flanking sequences will be appended.
        flank_length (int): Length of the flanking sequence to extract.
    """
    with open(pfm_file) as motif_file:
        all_motifs = list(motifs.parse(motif_file, "jaspar"))
    
    with open(output_file, "a") as output_handle:
        for motif in all_motifs:
            for record in SeqIO.parse(fasta_file, "fasta"):
                sequence = str(record.seq)
                
                for pos, _ in motif.pssm.search(sequence, threshold=0.9):  # Adjust threshold as needed
                    start, end = pos, pos + len(motif)
                    
                    # Extract left and right flanking sequences
                    left_flank = sequence[start - flank_length:start]
                    right_flank = sequence[end:end + flank_length]
                    
                    # Skip if the flank is shorter than required
                    if len(left_flank) < flank_length or len(right_flank) < flank_length:
                        continue
                    
                    # Write left flank
                    output_handle.write(
                        f">{record.id}_{start}_{end}_left\n{left_flank}\n"
                    )
                    
                    # Write right flank
                    output_handle.write(
                        f">{record.id}_{start}_{end}_right\n{right_flank}\n"
                    )
            
            print(f"Flanking sequences for motif {motif.matrix_id} appended to {output_file}")
