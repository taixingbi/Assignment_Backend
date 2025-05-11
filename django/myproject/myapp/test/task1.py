import os
import sys
import unittest
import django
from unittest.mock import patch
from django.core.cache import cache

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

# Set up Django environment manually if running outside manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myapp.tasks import fetch_sequence

class FetchSequenceTaskTests(unittest.TestCase):

    def setUp(self):
        cache.clear()
@patch("myapp.tasks.requests.get")
def test_fetch_sequence_from_api(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = ">header\nACGTACGT"

    result = fetch_sequence.run("123")
    print("0000" + result["sequence"])
    self.assertEqual(result["source"], "downloaded")
    self.assertEqual(result["sequence"], "ACGTACGT")
    self.assertEqual(cache.get("fasta:123"), "ACGTACGT")

if __name__ == "__main__":
    unittest.main()
