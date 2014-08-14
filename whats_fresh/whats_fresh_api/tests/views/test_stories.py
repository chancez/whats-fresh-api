from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class StoriesTestCase(TestCase):
    fixtures = ['whats_fresh_api/tests/testdata/test_fixtures.json']

    def setUp(self):
        self.expected_json = """
{
    "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
    },
    "story": "These are the voyages of the Starfish Enterblub; her five year mission -- to seek out new fish and new fishilizations..."
}"""

    def test_url_endpoint(self):
        url = reverse('story-details', kwargs={'id': '1'})
        self.assertEqual(url, '/stories/1')

    def test_json_equals(self):
        c = Client()
        response = c.get(reverse('story-details', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)
        self.assertTrue(parsed_answer == expected_answer)

    def test_missing_story_id(self):
        expected_error = """
{
  "error": {
    "error_status": true,
    "error_text": "Story with id 999 not found!",
    "error_name": "Story Not Found",
    "error_level": "Important"
  }
}"""
        c = Client()
        response = c.get(reverse('story-details', kwargs={'id': '999'}))
        self.assertTrue(response.status_code == 200)

        parsed_answer = json.loads(response.content)
        expected_answer = json.loads(expected_error)
        self.assertTrue(parsed_answer == expected_answer)
