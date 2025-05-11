# myapp/tasks.py

from celery import shared_task, chord
from myapp.get_sequence import fetch_write_sequence
from myapp.models import NucleotideChunk
from django.core.cache import cache
from collections import defaultdict
import re

@shared_task
def fetch_sequence_task(nucleotide_id):
    fetch_write_sequence(nucleotide_id)
    return nucleotide_id

@shared_task
def search_chunk_task(chunk_data, pattern, offset):
    regex = re.compile(pattern)
    matches = [(m.start() + offset, m.group()) for m in regex.finditer(chunk_data)]
    return matches

@shared_task(name='myapp.tasks.combine_and_cache')  # Register task with explicit name
def combine_and_cache(results, nucleotide_id, pattern):
    grouped = defaultdict(list)
    for match_list in results:
        for pos, match in match_list:
            grouped[match].append(pos)

    result = dict(grouped)
    cache_key = f"match:{nucleotide_id}:{pattern}"
    cache.set(cache_key, result, timeout=60 * 60)  # 1 hour TTL

    return result

def run_job(nucleotide_id, pattern):
    chunks = list(
        NucleotideChunk.objects
        .filter(sequence_id=nucleotide_id)
        .order_by("chunk_index")
        .values_list("chunk_data", flat=True)
    )

    tasks = []
    offset = 0
    for chunk_data in chunks:
        tasks.append(search_chunk_task.s(chunk_data, pattern, offset))
        offset += len(chunk_data)

    return chord(tasks)(combine_and_cache.s(nucleotide_id, pattern))
