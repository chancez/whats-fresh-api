from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class PreparationsTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.maxDiff = None
        self.expected_preparation = """
{
    "error": {
        "status": false,
        "name": null,
        "text": null,
        "debug": null,
        "level": null
    },
    "id": 1,
    "name": "Live",
    "description": "The food goes straight from sea to you with live food, sitting in saltwater tanks!",
    "additional_info": "Live octopus requires a locking container"
}"""

    def test_url_endpoint(self):
        url = reverse('preparation-details', kwargs={'id': '1'})
        self.assertEqual(url, '/1/preparations/1')

    def test_preparation_endpoint(self):
        response = self.client.get(
            reverse('preparation-details', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_preparation)
        self.assertEqual(parsed_answer, expected_answer)
