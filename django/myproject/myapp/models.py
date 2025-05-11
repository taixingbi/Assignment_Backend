from django.db import models

class NucleotideChunk(models.Model):
    id = models.BigAutoField(primary_key=True)  # unique row ID
    sequence_id = models.BigIntegerField()      # your nucleotide_id
    chunk_index = models.IntegerField()
    chunk_data = models.TextField()

    class Meta:
        unique_together = ('sequence_id', 'chunk_index')
