import pybedtools
from Bio import SeqIO

def extract_peak_sequences(bed_file, genome_file, output_fasta, overwrite='w'):
    """
    Extracts sequences of peaks from the BED file using the reference genome.

    Args:
        bed_file (str): Path to the BED file.
        genome_file (str): Path to the genome FASTA file.
        output_fasta (str): Path to save the extracted peak sequences as a FASTA file.
    """
    bed = pybedtools.BedTool(bed_file)
    genome_reference = SeqIO.to_dict(SeqIO.parse(genome_file, 'fasta'))
    
    with open(output_fasta, overwrite) as fasta_output:
        for peak in bed:
            chrom = peak.chrom
            start = int(peak.start)
            end = int(peak.end)
            
            peak_sequence = genome_reference[chrom].seq[start:end]
            fasta_output.write(f">{chrom}:{start}-{end}\n{peak_sequence}\n")
