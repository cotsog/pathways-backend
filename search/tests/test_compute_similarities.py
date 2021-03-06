from django.test import TestCase
from search.compute_similarities import (to_task_ids_and_descriptions,
                                         to_service_ids_and_descriptions,
                                         compute_similarities)
from human_services.services.models import Service
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import a_string


class TestTaskSimilarityScore(TestCase):
    def setUp(self):
        self.task_id = a_string()
        self.english_task_title = a_string()
        self.english_task_description = a_string()
        self.data = {
            'taskMap': {
                self.task_id: {
                    'completed': False,
                    'id': self.task_id,
                    'title': {
                        'en': self.english_task_title,
                    },
                    'description': {
                        'en': self.english_task_description
                    }
                }
            }
        }
        self.organization = OrganizationBuilder().create()

    def test_getting_ids_for_task_returns_task_id(self):
        ids, _ = to_task_ids_and_descriptions(self.data)
        self.assertEqual(ids[0], self.task_id)

    def test_converts_task_id_to_slug(self):
        self.data['taskMap'][self.task_id]['id'] = 'This is the id'
        ids, _ = to_task_ids_and_descriptions(self.data)
        self.assertEqual(ids[0], 'this-is-the-id')

    def test_getting_description_for_task_returns_task_title_and_description(self):
        _, descriptions = to_task_ids_and_descriptions(self.data)
        self.assertEqual(descriptions[0],
                         self.english_task_title + ' ' + self.english_task_description)

    def test_getting_id_for_service_returns_id(self):
        service = ServiceBuilder(self.organization).create()
        ids, _ = to_service_ids_and_descriptions(Service.objects.all())
        self.assertEqual(ids[0], service.id)

    def test_getting_description_for_service_returns_name_and_description(self):
        name = a_string()
        description = a_string()
        ServiceBuilder(self.organization).with_name(name).with_description(description).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertEqual(descriptions[0], name + ' ' + description)

    def test_computing_similarity_matrix(self):
        similarity_matrix = compute_similarities(['this is a bit of text',
                                                  'this is a similar bit of text',
                                                  'now for something different'])
        self.assertGreater(similarity_matrix[0, 0], 0.99)
        self.assertGreater(similarity_matrix[0, 1], 0.85)
        self.assertLess(similarity_matrix[0, 2], 0.10)

    def test_removes_local_phone_numbers_from_description(self):
        description_with_phone_numbers = 'Call 778-123-4567 or 604-123-4567 for more information.'
        description_without_phone_numbers = ('Call  or  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])
    
    def test_removes_international_phone_numbers_from_description(self):
        description_with_phone_numbers = 'Call 1-800-123-4567 for more information.'
        description_without_phone_numbers = ('Call  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_removes_phone_numbers_in_brackets_from_description(self):
        description_with_phone_numbers = 'Call 1-(800)-123-4567 or (604)-123-4567 for more information.'
        description_without_phone_numbers = ('Call  or  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_removes_phone_numbers_beginning_with_plus_sign_from_description(self):
        description_with_phone_numbers = 'Call +1-800-123-4567 or +604-123-4567 for more information.'
        description_without_phone_numbers = ('Call  or  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_removes_phone_numbers_beginning_with_plus_sign_and_two_numbers_from_description(self):
        description_with_phone_numbers = 'Call +49-800-123-4567 for more information.'
        description_without_phone_numbers = ('Call  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])
    
    def test_does_not_remove_numbers_that_are_not_phone_numbers(self):
        description_with_numbers = 'In 2017 the Canadian population was approximately 36,710,0000.'
        expected_description = ('In 2017 the Canadian population was approximately 36,710,0000.')
        ServiceBuilder(self.organization).with_description(description_with_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(expected_description, descriptions[0])