import os
import sys
import django

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

# Set up Django environment manually if running outside manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myapp.tasks import run_job, fetch_sequence, regex_search

if __name__ == "__main__":
    nucleotide_id = "30271926"
    pattern = "AATCGA|GGCAT"

    result1 = fetch_sequence(nucleotide_id)  # run task1 directly
    print("Sequence Fetch Result:", result1)

    result2 = regex_search(nucleotide_id, pattern)  # run task2 directly
    print("Regex Search Result:", result2)

    # run_job(nucleotide_id, pattern)

