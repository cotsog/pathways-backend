from django.core import exceptions
from django.db import IntegrityError
from django.test import TestCase
from taxonomies import models
from taxonomies.tests.helpers import TaxonomyTermBuilder


def validate_save_and_reload(taxonomy_term):
    taxonomy_term.save()
    return models.TaxonomyTerm.objects.get(pk=taxonomy_term.pk)


class TestTaxonomyModel(TestCase):
    def test_has_vocabulary_field(self):
        vocabulary = 'the_vocabulary'
        taxonomy_term = TaxonomyTermBuilder().with_vocabulary(vocabulary).build()
        taxonomy_term_from_db = validate_save_and_reload(taxonomy_term)
        self.assertEqual(taxonomy_term_from_db.vocabulary, vocabulary)

    def test_vocabulary_cannot_be_none(self):
        vocabulary = None
        taxonomy_term = TaxonomyTermBuilder().with_vocabulary(vocabulary).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_vocabulary_cannot_be_empty(self):
        vocabulary = ''
        taxonomy_term = TaxonomyTermBuilder().with_vocabulary(vocabulary).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_vocabulary_cannot_contain_space(self):
        vocabulary = 'the vocabulary'
        taxonomy_term = TaxonomyTermBuilder().with_vocabulary(vocabulary).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_has_name_field(self):
        name = 'the_name'
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        taxonomy_term_from_db = validate_save_and_reload(taxonomy_term)
        self.assertEqual(taxonomy_term_from_db.name, name)

    def test_name_cannot_be_none(self):
        name = None
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_name_cannot_be_empty(self):
        name = ''
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_name_cannot_contain_space(self):
        name = 'the name'
        taxonomy_term = TaxonomyTermBuilder().with_name(name).build()
        with self.assertRaises(exceptions.ValidationError):
            taxonomy_term.full_clean()

    def test_saving_two_taxonomies_with_same_vocabulary_and_different_name(self):
        vocabulary = 'the_vocabulary'
        name_1 = 'the_name_1'
        name_2 = 'the_name_2'

        taxonomy_term1 = TaxonomyTermBuilder().with_vocabulary(vocabulary).build()
        taxonomy_term1.name = name_1
        taxonomy_term1.save()

        taxonomy_term2 = TaxonomyTermBuilder().with_vocabulary(vocabulary).build()
        taxonomy_term2.name = name_2
        taxonomy_term2.save()

        self.assertNotEqual(taxonomy_term1.pk, taxonomy_term2.pk)

    def test_saving_two_taxonomies_with_same_name_and_different_vocabulary(self):
        vocabulary_1 = 'the_vocabulary_1'
        vocabulary_2 = 'the_vocabulary_2'
        name = 'the_name'

        taxonomy_term1 = TaxonomyTermBuilder().with_name(name).build()
        taxonomy_term1.vocabulary = vocabulary_1
        taxonomy_term1.save()

        taxonomy_term2 = TaxonomyTermBuilder().with_name(name).build()
        taxonomy_term2.vocabulary = vocabulary_2
        taxonomy_term2.save()

        self.assertNotEqual(taxonomy_term1.pk, taxonomy_term2.pk)

    def test_saving_two_taxonomies_with_same_name_and_vocabulary_fails_with_integrity_error(self):
        vocabulary = 'the_vocabulary'
        name = 'the_name'

        taxonomy_term1 = TaxonomyTermBuilder().with_vocabulary(vocabulary).with_name(name).build()
        taxonomy_term1.save()

        taxonomy_term2 = TaxonomyTermBuilder().with_vocabulary(vocabulary).with_name(name).build()
        with self.assertRaises(IntegrityError):
            taxonomy_term2.save()
