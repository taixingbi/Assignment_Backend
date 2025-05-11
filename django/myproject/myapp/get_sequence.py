import requests
from myapp.models import NucleotideChunk

# Each chunk is 5MB
CHUNK_SIZE = 5 * 1024 * 1024  # bytes

def fetch_write_sequence(nucleotide_id):
    """
    Fetches a nucleotide sequence from NCBI and saves it to the database in 5MB chunks.
    """
    if NucleotideChunk.objects.filter(sequence_id=nucleotide_id).exists():
        print(f"Sequence ID {nucleotide_id} already exists in DB. Skipping fetch.")
        return

    response = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        params={
            "db": "nucleotide",
            "id": nucleotide_id,
            "rettype": "fasta",
            "retmode": "text"
        },
        stream=True
    )

    sequence_parts = []
    for line in response.iter_lines(decode_unicode=True):
        if not line.startswith('>'):
            sequence_parts.append(line)
    sequence = ''.join(sequence_parts)

    # Clear existing chunks for this sequence ID
    NucleotideChunk.objects.filter(sequence_id=nucleotide_id).delete()

    # Split and save in chunks
    chunks = [sequence[i:i + CHUNK_SIZE] for i in range(0, len(sequence), CHUNK_SIZE)]
    objs = [
        NucleotideChunk(sequence_id=nucleotide_id, chunk_index=i, chunk_data=chunk)
        for i, chunk in enumerate(chunks)
    ]
    NucleotideChunk.objects.bulk_create(objs)

    print(f"Saved {len(objs)} chunks for sequence ID {nucleotide_id} (total length: {len(sequence)} bp)")

