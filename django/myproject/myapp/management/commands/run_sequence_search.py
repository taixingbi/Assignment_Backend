import json
from django.core.management.base import BaseCommand
from myapp.tasks import run_job
from celery.result import AsyncResult
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Run sequence regex search using a nucleotide ID and pattern'

    def add_arguments(self, parser):
        parser.add_argument('nucleotide_id', type=str, help='The NCBI nucleotide ID')
        parser.add_argument('pattern', type=str, help='Regex pattern to search for')
        parser.add_argument('--output', type=str, default='', help='Optional output file path')

    def handle(self, *args, **options):
        nucleotide_id = options['nucleotide_id']
        pattern = options['pattern']
        output_path = options['output']

        self.stdout.write(f"Running search on ID {nucleotide_id} with pattern '{pattern}'")

        result = run_job(nucleotide_id, pattern)

        self.stdout.write("Waiting for results...")
        final_result = AsyncResult(result.id).get(timeout=600)

        # Prepare output path
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_results_{nucleotide_id}_{timestamp}.json"
            output_path = os.path.join(os.getcwd(), filename)

        with open(output_path, "w") as f:
            json.dump(final_result, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Search complete. Results saved to {output_path}"))
